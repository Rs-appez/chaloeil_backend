
from .models import Question,Category,Answer
from rest_framework import serializers

class QuestionSerializer(serializers.ModelSerializer):

    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Question
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'