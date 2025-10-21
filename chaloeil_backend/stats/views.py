from django.shortcuts import render

from question.models import QuestionsOfTheDay
from .models import Statistic


def index(request):
    stats = Statistic.objects.all()
    data = Statistic.get_pourcentage(stats)
    return render(request, "index1.html", {"data": data})


def qotd_stats(request):
    qotd = QuestionsOfTheDay.objects.last()
    if not qotd:
        return render(request, "index1.html", {"data": []})

    stats = Statistic.objects.filter(
        question__questionsofthedayquestion__questions_of_the_day=qotd
    )
    data = Statistic.get_pourcentage(stats)
    return render(request, "index1.html", {"data": data})
