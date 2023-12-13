from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated , IsAdminUser

from .serializers import QuestionSerializer , CategorySerializer , AnswerSerializer

from .models import Question , Answer , Category

class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False, methods=['get'],url_path= 'random_question',permission_classes=[IsAuthenticated])
    def get_random_question(self, request, pk=None):
        category = request.query_params.get('category')
        nb = int(request.query_params.get('number')) or 1

        question = Question.objects.order_by('?').all()[:nb] if not category  else Question.objects.filter(categories__category_text__iexact=category).order_by('?').all()[:nb]
        serializer = QuestionSerializer(question, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'],url_path= 'questions_with',permission_classes=[IsAuthenticated])
    def get_questions_with(self, request, pk=None):
        text = request.query_params.get('text')
        questions = Question.objects.filter(question_text__iexact=text)
        answers = Answer.objects.filter(question__in=questions, is_correct=True)
        serializer = AnswerSerializer(answers, context={'request': request}, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'],url_path= 'questions_without_answer',permission_classes=[IsAuthenticated])
    def get_questions_without_answer(self, request, pk=None):
        questions = Question.objects.all()
        questions_without_answers = [question for question in questions if all(answer.is_correct is False for answer in question.answers.all())]
        serializer = QuestionSerializer(questions_without_answers, context={'request': request}, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# class AnswerViewSet(viewsets.ModelViewSet):
    
#     queryset = Answer.objects.all()
#     serializer_class = AnswerSerializer

