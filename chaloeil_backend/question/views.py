from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import QuestionSerializer , CategorySerializer , AnswerSerializer

from .models import Question , Answer , Category

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False, methods=['get'],url_path= 'random_question')
    def get_random_question(self, request, pk=None):
        question = Question.objects.order_by('?').first()
        serializer = QuestionSerializer(question, context={'request': request})
        return Response(serializer.data)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# class AnswerViewSet(viewsets.ModelViewSet):
    
#     queryset = Answer.objects.all()
#     serializer_class = AnswerSerializer

