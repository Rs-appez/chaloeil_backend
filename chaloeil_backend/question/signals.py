from django.db.models.signals import post_delete
from django.dispatch import receiver

from question.models import (
    QuestionsOfTheDay,
    QuestionsOfTheDayQuestion,
)


@receiver(post_delete, sender=QuestionsOfTheDayQuestion)
def update_qotd_question_count(sender, instance, **kwargs):
    qotd = instance.questions_of_the_day
    qotd.number_of_questions = QuestionsOfTheDayQuestion.objects.filter(
        questions_of_the_day=qotd
    ).count()
    _ = QuestionsOfTheDay.objects.filter(pk=qotd.pk).update(
        number_of_questions=qotd.number_of_questions
    )
