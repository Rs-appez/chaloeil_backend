
from .models import Question,Category,Answer,Level
from rest_framework import serializers

class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    id_question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), source='question')
    class Meta:
        model = Answer
        fields = ['answer_text','is_correct','id_question']
        
class QuestionSerializer(serializers.ModelSerializer):

    categories = serializers.StringRelatedField(many=True)
    answers = AnswerSerializer(many=True)
    level = serializers.StringRelatedField(many=False)

    class Meta:
        model = Question
        fields = ['question_text','categories','level','answers', 'image_url']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'



