from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from .models import Motorcycle, Auction, Bid

User = get_user_model()

class AuctionApiTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username="seller", password="StrongPass123!")
        self.bidder = User.objects.create_user(username="bidder", password="StrongPass123!")
        now = timezone.now()
        bike = Motorcycle.objects.create(
            seller=self.seller, title="Test bike", make="Honda", model="CB", year=2022,
            mileage_km=5000, description="Test motorcycle"
        )
        self.auction = Auction.objects.create(
            motorcycle=bike, start_time=now-timedelta(minutes=1),
            end_time=now+timedelta(hours=1), starting_price=Decimal("10000.00"),
            minimum_increment=Decimal("100.00")
        )
        self.client = APIClient()
        token = self.client.post("/api/auth/token/", {
            "username": "bidder", "password": "StrongPass123!"
        }, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.data['access']}")

    def test_auction_status_is_live(self):
        self.assertEqual(self.auction.status, Auction.Status.LIVE)

    def test_bid_at_starting_price_is_accepted(self):
        response = self.client.post(f"/api/auctions/{self.auction.id}/bid/",
                                    {"amount": "10000.00"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Bid.objects.filter(auction=self.auction).count(), 1)

    def test_bid_below_minimum_is_rejected(self):
        response = self.client.post(f"/api/auctions/{self.auction.id}/bid/",
                                    {"amount": "9999.00"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Bid.objects.filter(auction=self.auction).count(), 0)

    def test_seller_cannot_bid_on_own_listing(self):
        self.client.force_authenticate(user=self.seller)
        response = self.client.post(f"/api/auctions/{self.auction.id}/bid/",
                                    {"amount": "10000.00"}, format="json")
        self.assertEqual(response.status_code, 403)
