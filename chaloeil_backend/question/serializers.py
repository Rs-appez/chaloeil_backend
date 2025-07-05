from .models import Question, Category, Answer, Level, QuestionsOfTheDay
from rest_framework import serializers


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    id_question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(), source="question"
    )

    class Meta:
        model = Answer
        fields = ["id", "answer_text", "is_correct", "id_question", "emoticon"]


class QuestionSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)
    answers = AnswerSerializer(many=True)
    level = serializers.StringRelatedField(many=False)

    class Meta:
        model = Question
        fields = [
            "id",
            "question_text",
            "categories",
            "level",
            "answers",
            "image_url",
            "shuffle_answers",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class QuestionsOfTheDaySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = QuestionsOfTheDay
        fields = ["id", "questions", "number_of_questions", "date"]
