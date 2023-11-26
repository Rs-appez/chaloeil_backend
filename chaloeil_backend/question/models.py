from django.db import models

class Question(models.Model):
    question_text = models.TextField()
    categories = models.ManyToManyField('Category')
    level = models.IntegerField()
    image_url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.answer_text

class Category(models.Model):
    category_text = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.category_text

