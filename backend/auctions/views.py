import logging
from decimal import Decimal
from django.db import transaction
from django.db.models import Prefetch
from django.utils import timezone
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Motorcycle, Auction, Bid
from .serializers import RegisterSerializer, MotorcycleSerializer, AuctionSerializer, BidSerializer, PlaceBidSerializer

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class HealthView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    def get(self, request):
        return Response({"status": "ok", "timestamp": timezone.now().isoformat()})

class AuctionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuctionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Auction.objects.select_related("motorcycle", "motorcycle__seller").prefetch_related("bids", "bids__bidder")
        state = self.request.query_params.get("status")
        if state in [Auction.Status.SCHEDULED, Auction.Status.LIVE, Auction.Status.ENDED]:
            now = timezone.now()
            if state == Auction.Status.SCHEDULED:
                qs = qs.filter(start_time__gt=now)
            elif state == Auction.Status.LIVE:
                qs = qs.filter(start_time__lte=now, end_time__gt=now)
            else:
                qs = qs.filter(end_time__lte=now)
        return qs

    @action(detail=True, methods=["get"])
    def bids(self, request, pk=None):
        auction = self.get_object()
        bids = auction.bids.select_related("bidder").order_by("-created_at")[:100]
        return Response(BidSerializer(bids, many=True).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def bid(self, request, pk=None):
        serializer = PlaceBidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]
        with transaction.atomic():
            # Row lock serializes bid attempts for this auction on PostgreSQL.
            auction = Auction.objects.select_for_update().select_related("motorcycle").get(pk=pk)
            now = timezone.now()
            if now < auction.start_time:
                raise ValidationError({"detail": "This auction has not started."})
            if now >= auction.end_time:
                raise ValidationError({"detail": "This auction has ended."})
            if auction.motorcycle.seller_id == request.user.id:
                raise PermissionDenied("You cannot bid on your own motorcycle.")
            highest = Bid.objects.filter(auction=auction).order_by("-amount", "-created_at").first()
            minimum = highest.amount + auction.minimum_increment if highest else auction.starting_price
            if amount < minimum:
                raise ValidationError({"amount": f"Bid must be at least {minimum}."})
            bid = Bid.objects.create(auction=auction, bidder=request.user, amount=amount)
            logger.info("bid_placed auction_id=%s bid_id=%s user_id=%s amount=%s",
                        auction.id, bid.id, request.user.id, amount)
        return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)
