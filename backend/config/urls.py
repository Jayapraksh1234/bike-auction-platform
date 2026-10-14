from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from auctions.views import RegisterView, HealthView
from django.http import JsonResponse
def home(request):
    return JsonResponse({
        "message": "Bike Auction Platform API",
        "status": "running",
        "auctions": "/api/auctions/",
        "health": "/api/health/",
        "admin": "/admin/",
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("auctions.urls")),
    path("api/health/", HealthView.as_view(), name="health"),
]
