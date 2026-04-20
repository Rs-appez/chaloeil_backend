from django.contrib.auth.decorators import permission_required
from django.db.models import Count
from django.shortcuts import render
from question.models import QuestionsOfTheDay

from .models import QotdStatistic, Statistic
from .serializers import GlobalLeaderboardSerializer


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
    stats = QotdStatistic.objects.annotate(
        session_count=Count("player__sessionstatistic")
    ).order_by("-score")
    data = GlobalLeaderboardSerializer(stats, many=True).data
    return render(request, "leaderboard.html", {"participants": data})
