from django.urls import path, include
from . import views_api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"statistics", views_api.StatisticsViewSet, basename="statistics")
router.register(r"teams", views_api.TeamViewSet, basename="team")
router.register(r"players", views_api.PlayerViewSet, basename="player")

urlpatterns = [
    path("api/", include(router.urls)),
]
