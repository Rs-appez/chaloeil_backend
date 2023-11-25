
from .models import Question,Category,Answer
from rest_framework import serializers

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['answer_text','is_correct']
        
class QuestionSerializer(serializers.ModelSerializer):

    categories = serializers.StringRelatedField(many=True)
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['question_text','categories','level','answers']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

