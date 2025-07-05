from django.db import models
from typing import List


class Question(models.Model):
    question_text = models.TextField()
    categories = models.ManyToManyField("Category")
    level = models.ForeignKey("Level", on_delete=models.PROTECT)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    shuffle_answers = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    emoticon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.answer_text


class Category(models.Model):
    category_text = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.category_text


class Level(models.Model):
    level_text = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.level_text


class QuestionsOfTheDay(models.Model):
    questions = models.ManyToManyField(
        Question, related_name="questions_of_the_day")
    number_of_questions = models.PositiveIntegerField(default=20)
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.date} - {self.questions}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save first to get an ID
        questions = self.__get_random_questions_not_in_qotd(
            self.number_of_questions)
        self.questions.set(questions)

    def __get_random_questions_not_in_qotd(self, count: int) -> List[Question]:
        used_questions = list(QuestionsOfTheDay.objects.values_list(
            "questions", flat=True))
        questions = Question.objects.exclude(
            id__in=used_questions).order_by("?")[:count]
        return questions
