from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets

from .serializers import QuestionSerializer , CategorySerializer , AnswerSerializer

from .models import Question , Answer , Category

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer



class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AnswerViewSet(viewsets.ModelViewSet):
    
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

