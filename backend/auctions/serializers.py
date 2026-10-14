from django.contrib.auth import get_user_model
from decimal import Decimal
from rest_framework import serializers
from .models import Motorcycle, Auction, Bid

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class MotorcycleSerializer(serializers.ModelSerializer):
    seller_username = serializers.CharField(source="seller.username", read_only=True)
    class Meta:
        model = Motorcycle
        fields = ("id", "seller", "seller_username", "title", "make", "model", "year",
                  "mileage_km", "description", "image_url", "created_at")
        read_only_fields = ("id", "seller", "seller_username", "created_at")

class BidSerializer(serializers.ModelSerializer):
    bidder_username = serializers.CharField(source="bidder.username", read_only=True)
    class Meta:
        model = Bid
        fields = ("id", "bidder_username", "amount", "created_at")
        read_only_fields = fields

class AuctionSerializer(serializers.ModelSerializer):
    motorcycle = MotorcycleSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
    current_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    minimum_next_bid = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    bid_count = serializers.IntegerField(source="bids.count", read_only=True)
    highest_bidder = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ("id", "motorcycle", "start_time", "end_time", "starting_price",
                  "minimum_increment", "status", "current_price", "minimum_next_bid",
                  "bid_count", "highest_bidder", "created_at")
        read_only_fields = fields

    def get_highest_bidder(self, obj):
        bid = obj.highest_bid
        return bid.bidder.username if bid else None

class PlaceBidSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))
