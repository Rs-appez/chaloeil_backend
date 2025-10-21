from django.shortcuts import render

from question.models import QuestionsOfTheDay, QuestionsOfTheDayQuestion
from .models import Statistic
from .utils import get_pourcentage


def index(request):
    stats = Statistic.objects.select_related("question")
    data = get_pourcentage(stats)
    return render(request, "index1.html", {"data": data})


def qotd_stats(request):
    qotd = QuestionsOfTheDay.objects.last()
    if not qotd:
        return render(request, "index1.html", {"data": []})

    questions = QuestionsOfTheDayQuestion.objects.filter(
        questions_of_the_day=qotd
    ).select_related("question")

    stats = Statistic.objects.filter(
        question__in=[q.question for q in questions]
    ).select_related("question")
    data = get_pourcentage(stats)
    return render(request, "index1.html", {"data": data})
