from django.db.models import QuerySet
from collections import defaultdict


def get_pourcentage(stats: QuerySet):
    grouped = defaultdict(list)
    for stat in stats:
        grouped[stat.question].append(stat)

    questions = {}
    for question, stat_list in grouped.items():
        questions[question] = sum(
            [stat.get_correct_percentage() for stat in stat_list]
        ) / len(stat_list)

    return sorted(questions.items(), key=lambda item: item[1], reverse=True)
