from django.contrib.auth.decorators import permission_required
from django.db.models import Count, F, Window
from django.db.models.functions import Rank
from django.shortcuts import get_object_or_404, render
from question.models import QuestionOfTheDaySession, QuestionsOfTheDay

from .models import QotdStatistic, SessionStatistic, Statistic
from .serializers import GlobalLeaderboardSerializer, LeaderboardSerializer


@permission_required("chaloeil_backend.view_statistic")
def index(request):
    stats = Statistic.objects.all()
    data = Statistic.get_pourcentage(stats)
    return render(request, "index1.html", {"data": data})


@permission_required("chaloeil_backend.view_statistic")
def qotd_stats(request):
    qotd = QuestionsOfTheDay.objects.last()
    if not qotd:
        return render(request, "index1.html", {"data": []})

    stats = Statistic.objects.filter(
        question__questionsofthedayquestion__questions_of_the_day=qotd
    )
    data = Statistic.get_pourcentage(stats)
    return render(request, "index1.html", {"data": data})


def leaderboard_global(request):
    stats = (
        QotdStatistic.objects.exclude(player__name="appez")
        .annotate(rank=Window(expression=Rank(), order_by=F("score").desc()))
        .annotate(session_count=Count("player__sessionstatistic"))
        .order_by("-score")
    )
    data = GlobalLeaderboardSerializer(stats, many=True).data
    return render(request, "leaderboard.html", {"participants": data})


def leaderboard(request, qotd_id):
    session = get_object_or_404(QuestionOfTheDaySession, id=qotd_id)
    stats = (
        SessionStatistic.objects.filter(session=session)
        .exclude(player__name="appez")
        .annotate(rank=Window(expression=Rank(), order_by=F("score").desc()))
        .order_by("-score")
    )
    data = LeaderboardSerializer(stats, many=True).data
    return render(
        request, "sessionboard.html", {"participants": data, "session": session}
    )
