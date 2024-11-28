from django.db import  models
from django.forms import ValidationError

def case_unsensitive_validator(value):
    if Word.objects.filter(word__iexact=value).exists():
        raise ValidationError("The word already exists.")

class Word(models.Model):
    word = models.CharField(max_length=100, unique=True, validators=[case_unsensitive_validator])
    length = models.IntegerField(editable=False)

    def save(self, *args, **kwargs):
        self.word = self.word.lower()
        self.length = len(self.word)
        super(Word, self).save(*args, **kwargs)
            

    def __str__(self):
        return self.word