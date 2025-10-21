from .models import (
    Question,
    Category,
    Answer,
    Level,
    QuestionsOfTheDay,
    QuestionsOfTheDayQuestion,
)
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
    image_url = serializers.SerializerMethodField()

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

    def get_image_url(self, obj):
        return obj.get_image_url()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class QuestionsOfTheDayQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = QuestionsOfTheDayQuestion
        fields = ["question", "order"]


class QuestionsOfTheDaySerializer(serializers.ModelSerializer):
    questions = QuestionsOfTheDayQuestionSerializer(many=True)

    class Meta:
        model = QuestionsOfTheDay
        fields = ["id", "questions", "number_of_questions", "date"]
