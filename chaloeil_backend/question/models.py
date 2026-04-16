from typing import override

from chaloeil_backend.storage_backends import QuestionMediaStorage, rename_file
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.TextField()
    categories = models.ManyToManyField("Category")
    level = models.ForeignKey("Level", on_delete=models.PROTECT)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(
        upload_to=rename_file, storage=QuestionMediaStorage(), blank=True, null=True
    )
    shuffle_answers = models.BooleanField(default=True)
    need_review = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)

    @override
    def __str__(self) -> str:
        return self.question_text

    def get_image_url(self) -> str:
        if self.image:
            return self.image.url
        return self.image_url


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    emoticon = models.CharField(max_length=100, blank=True, null=True)

    @override
    def __str__(self) -> str:
        return self.answer_text


class Category(models.Model):
    category_text = models.CharField(max_length=200, unique=True)

    @override
    def __str__(self) -> str:
        return self.category_text


class Level(models.Model):
    level_text = models.CharField(max_length=200, unique=True)

    @override
    def __str__(self) -> str:
        return self.level_text


class QuestionOfTheDaySession(models.Model):
    date = models.DateTimeField()
    active = models.BooleanField(default=True)
    number_of_questions = models.PositiveSmallIntegerField(default=1)

    @override
    def __str__(self) -> str:
        return f"Session of {self.date}"


class QuestionsOfTheDay(models.Model):
    number_of_questions: models.PositiveSmallIntegerField[int, int] = (
        models.PositiveSmallIntegerField(default=20)
    )
    time_to_answer_hour = models.PositiveSmallIntegerField(default=8)
    date = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(
        QuestionOfTheDaySession,
        on_delete=models.CASCADE,
        related_name="qotd",
        null=True,
    )

    @override
    def __str__(self) -> str:
        return f"{self.date}"

    @override
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            self.session = QuestionOfTheDaySession.objects.filter(
                active=True, date__lt=timezone.now()
            ).last()
            if not self.session:
                raise ValueError("No active session found for Questions of the Day")
            if (
                self.session.number_of_questions
                == QuestionsOfTheDay.objects.filter(session=self.session).count()
            ):
                raise ValueError(
                    "The number of questions for this session has already been reached"
                )

            super().save(*args, **kwargs)
            questions = self.__get_random_questions_not_in_qotd(
                self.number_of_questions
            )
            objects = [
                QuestionsOfTheDayQuestion(
                    questions_of_the_day=self,
                    question=question,
                    order=idx,
                )
                for idx, question in enumerate(questions)
            ]
            _ = QuestionsOfTheDayQuestion.objects.bulk_create(objects)

            self.number_of_questions = len(objects)
        else:
            self.number_of_questions = self.__get_nb_questions_in_qotd()
        super().save(update_fields=["number_of_questions", "session"])

    def __get_random_questions_not_in_qotd(self, count: int) -> list[Question]:
        return list(
            Question.objects.exclude(
                id__in=QuestionsOfTheDayQuestion.objects.filter(
                    questions_of_the_day__session=self.session
                ).values("question_id")
            ).order_by("?")[:count]
        )

    def __get_nb_questions_in_qotd(self) -> int:
        return QuestionsOfTheDayQuestion.objects.filter(
            questions_of_the_day=self
        ).count()


class QuestionsOfTheDayQuestion(models.Model):
    questions_of_the_day = models.ForeignKey(
        QuestionsOfTheDay, on_delete=models.CASCADE, related_name="questions"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    @override
    def __str__(self) -> str:
        return f"{self.questions_of_the_day} - {self.question.question_text}"
