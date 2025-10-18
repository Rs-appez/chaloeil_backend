import random
from datetime import datetime, timedelta

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from stats.models import PlayerQotd

from .models import Answer, Category, Question, QuestionsOfTheDay
from .serializers import (
    AnswerSerializer,
    CategorySerializer,
    QuestionSerializer,
    QuestionsOfTheDaySerializer,
)


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="random_question",
        permission_classes=[IsAuthenticated],
    )
    def get_random_question(self, request, pk=None):
        category = request.query_params.get("category")
        nb = (
            int(request.query_params.get("number"))
            if request.query_params.get("number") is not None
            else 1
        )
        id_range = request.query_params.get("id_range")

        if id_range:
            try:
                id_range = id_range.split("-")
                question = Question.objects.filter(id__range=(id_range[0], id_range[1]))
            except Exception:
                return Response({"error": "id_range parameter is invalid"}, status=400)
        else:
            question = (
                Question.objects.order_by("?").all()[:nb]
                if not category
                else Question.objects.filter(categories__category_text__iexact=category)
                .order_by("?")
                .all()[:nb]
            )

        serializer = QuestionSerializer(
            question, context={"request": request}, many=True
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="questions_with",
        permission_classes=[IsAuthenticated],
    )
    def get_questions_with(self, request, pk=None):
        text = request.query_params.get("text")

        if not text:
            return Response({"error": "text parameter is required"}, status=400)

        questions = Question.objects.filter(question_text__icontains=text)

        serializer = QuestionSerializer(
            questions, context={"request": request}, many=True
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="questions_without_answer",
        permission_classes=[IsAuthenticated],
    )
    def get_questions_without_answer(self, request, pk=None):
        questions = Question.objects.all()
        questions_without_answers = [
            question
            for question in questions
            if all(answer.is_correct is False for answer in question.answers.all())
        ]
        serializer = QuestionSerializer(
            questions_without_answers, context={"request": request}, many=True
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="questions_with_image",
        permission_classes=[IsAuthenticated],
    )
    def get_questions_with_image(self, request, pk=None):
        url = (
            request.query_params.get("url")
            if request.query_params.get("url") is not None
            else ""
        )
        questions = Question.objects.filter(
            image_url__isnull=False, image_url__icontains=url
        )
        page = self.paginate_queryset(questions)
        serializer = QuestionSerializer(page, context={"request": request}, many=True)

        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AnswerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class QuestionsOfTheDayViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = QuestionsOfTheDay.objects.all()
    serializer_class = QuestionsOfTheDaySerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="qotd",
        permission_classes=[IsAuthenticated],
    )
    def get_qotd(self, request, pk=None):
        """
        Get the Questions of the Day
        """
        player = request.query_params.get("player")
        if not player:
            return Response({"error": "Player not found"}, status=404)

        qotd = QuestionsOfTheDay.objects.last()
        if not qotd:
            return Response({"error": "No Questions of the Day found"}, status=404)

        is_player_answered = PlayerQotd.objects.filter(
            player__discord_id=player, question_of_the_day=qotd
        ).exists()

        if is_player_answered:
            return Response(
                {"error": "You have already answered today's Questions of the Day"},
                status=403,
            )

        today = datetime.now(qotd.date.tzinfo)
        if today > qotd.date + timedelta(hours=qotd.time_to_answer_hour):
            return Response(
                {"error": "Questions of the Day are not available yet"}, status=404
            )

        serializer = self.get_serializer(qotd)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        url_path="generate_qotd",
        permission_classes=[IsAdminUser],
    )
    def generate_qotd(self, request, pk=None):
        """
        Generate Questions of the Day.
        """
        try:
            number_of_questions = random.randint(8, 12)

            QuestionsOfTheDay.objects.create(number_of_questions=number_of_questions)

            return Response(
                {"message": "Questions of the Day generated successfully"}, status=201
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)
