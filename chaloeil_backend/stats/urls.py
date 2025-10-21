from django.urls import path, include
from . import views_api as api
from . import views as v

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"statistics", api.StatisticsViewSet, basename="statistics")
router.register(r"teams", api.TeamViewSet, basename="team")
router.register(r"players", api.PlayerViewSet, basename="player")
router.register(r"qotdStatistics", api.QotdStatisticViewSet, basename="qotd_statistics")


urlpatterns = [
    path("api/", include(router.urls)),
    path("", v.index, name="index"),
    path("qotd-stats/", v.qotd_stats, name="qotd_stats"),
]
