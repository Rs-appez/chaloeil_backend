from .models import QuestionsOfTheDay
import random

def create_questions_of_the_day():
    """
    Create or update the Questions of the Day.
    """
    number_of_questions = random.randint(15, 25)
    QuestionsOfTheDay(number_of_questions=number_of_questions).save()
