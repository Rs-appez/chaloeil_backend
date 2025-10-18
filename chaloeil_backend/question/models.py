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
    number_of_questions = models.PositiveIntegerField(default=20)
    time_to_answer_hour = models.PositiveIntegerField(default=8)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.date}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            questions = self.__get_random_questions_not_in_qotd(
                self.number_of_questions
            )
            for idx, question in enumerate(questions):
                QuestionsOfTheDayQuestion.objects.create(
                    questions_of_the_day=self, question=question, order=idx
                )

        self.number_of_questions = self.questions.count()
        super().save(update_fields=["number_of_questions"])

    def __get_random_questions_not_in_qotd(self, count: int) -> List[Question]:
        used_questions = QuestionsOfTheDayQuestion.objects.all().values("question")
        questions = Question.objects.exclude(id__in=used_questions).order_by(
            "?"
        )[:count]
        return questions


class QuestionsOfTheDayQuestion(models.Model):
    questions_of_the_day = models.ForeignKey(
        QuestionsOfTheDay, on_delete=models.CASCADE, related_name="questions"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.questions_of_the_day} - {self.question.question_text}"
