from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone

class Motorcycle(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="motorcycles")
    title = models.CharField(max_length=160)
    make = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    year = models.PositiveSmallIntegerField()
    mileage_km = models.PositiveIntegerField(default=0)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class Auction(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        LIVE = "live", "Live"
        ENDED = "ended", "Ended"

    motorcycle = models.OneToOneField(Motorcycle, on_delete=models.CASCADE, related_name="auction")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    starting_price = models.DecimalField(max_digits=12, decimal_places=2)
    minimum_increment = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("100.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]

    @property
    def status(self):
        now = timezone.now()
        if now < self.start_time:
            return self.Status.SCHEDULED
        if now >= self.end_time:
            return self.Status.ENDED
        return self.Status.LIVE

    @property
    def highest_bid(self):
        return self.bids.order_by("-amount", "-created_at").first()

    @property
    def current_price(self):
        bid = self.highest_bid
        return bid.amount if bid else self.starting_price

    @property
    def minimum_next_bid(self):
        bid = self.highest_bid
        return (bid.amount + self.minimum_increment) if bid else self.starting_price

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="bids")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["auction", "-amount", "-created_at"]),
            models.Index(fields=["bidder", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.auction_id}: {self.amount} by {self.bidder_id}"
