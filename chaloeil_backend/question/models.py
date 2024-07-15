from django.db import models

class Question(models.Model):
    question_text = models.TextField()
    categories = models.ManyToManyField('Category')
    level = models.ForeignKey('Level', on_delete=models.PROTECT)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    shuffle_answers = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    emoticon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.answer_text

class Category(models.Model):
    category_text = models.CharField(max_length=200,unique=True)

    def __str__(self) -> str:
        return self.category_text

class Level(models.Model):
    level_text = models.CharField(max_length=200,unique=True)

    def __str__(self) -> str:
        return self.level_text
