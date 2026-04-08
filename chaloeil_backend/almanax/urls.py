from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EconomyEntryViewSet

router = DefaultRouter()
router.register(r"economy-entries", EconomyEntryViewSet, basename="economy-entry")

urlpatterns = [
    path("api/", include(router.urls)),
]
