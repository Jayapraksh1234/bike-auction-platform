from django.contrib import admin
from .models import Motorcycle, Auction, Bid

class AuctionInline(admin.StackedInline):
    model = Auction
    extra = 0

@admin.register(Motorcycle)
class MotorcycleAdmin(admin.ModelAdmin):
    list_display = ("title", "make", "model", "year", "seller", "created_at")
    search_fields = ("title", "make", "model", "seller__username")
    inlines = [AuctionInline]

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "motorcycle", "start_time", "end_time", "starting_price")
    list_filter = ("start_time", "end_time")

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", "bidder", "amount", "created_at")
    readonly_fields = ("auction", "bidder", "amount", "created_at")
