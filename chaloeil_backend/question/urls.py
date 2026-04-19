from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"questions", views.QuestionViewSet, basename="question")
router.register(r"qotd", views.QuestionsOfTheDayViewSet, basename="qotd")
router.register(
    r"qotd-standalone",
    views.QuestionsOfTheDayStandaloneViewSet,
    basename="qotd-standalone",
)

urlpatterns = [
    path("", include(router.urls)),
]
