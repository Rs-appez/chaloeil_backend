import random
from datetime import datetime, timedelta

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    DjangoModelPermissions,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.request import Request
from stats.models import FlagReport, Player, PlayerQotd

from .models import Answer, Category, Question, QuestionsOfTheDay
from .serializers import (
    AnswerSerializer,
    CategorySerializer,
    QuestionSerializer,
    QuestionsOfTheDaySerializer,
    SimpleQuestionSerializer,
)


class QuestionViewSet(viewsets.ModelViewSet[Question]):
    permission_classes = [IsAdminUser]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="random_question",
        permission_classes=[IsAuthenticated],
    )
    def get_random_question(self, request: Request):
        category = request.query_params.get("category")
        nb = int(request.query_params.get("number", "1"))
        id_range = request.query_params.get("id_range")

        questions = Question.objects.exclude(need_review=True)
        if id_range:
            try:
                id_range = id_range.split("-")
                questions = questions.filter(id__range=(id_range[0], id_range[1]))
            except Exception:
                return Response({"error": "id_range parameter is invalid"}, status=400)
        if category:
            questions = questions.filter(categories__category_text__iexact=category)

        question = questions.order_by("?")[:nb]

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
    def get_questions_with(self, request: Request):
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
    def get_questions_without_answer(self, request: Request):
        questions = Question.objects.exclude(answers__is_correct=True)
        serializer = SimpleQuestionSerializer(
            questions, context={"request": request}, many=True
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="questions_with_image",
        permission_classes=[IsAuthenticated],
    )
    def get_questions_with_image(self, request: Request):
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

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def flag_for_review(self, request: Request, pk=None):
        player_id = request.data.get("player_id", None)
        if not player_id:
            return Response({"error": "User parameter is required"}, status=400)

        player = Player.objects.filter(discord_id=player_id).first()
        if not player:
            return Response({"error": "Player not found"}, status=404)

        question = self.get_object()
        question.need_review = True
        question.save(update_fields=["need_review"])
        _ = FlagReport.objects.create(question=question, player=player)

        return Response({"message": "Question flagged for review successfully"})


class CategoryViewSet(viewsets.ReadOnlyModelViewSet[Category]):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AnswerViewSet(viewsets.ModelViewSet[Answer]):
    permission_classes = [IsAdminUser]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class QuestionsOfTheDayViewSet(viewsets.ModelViewSet[QuestionsOfTheDay]):
    permission_classes = [IsAdminUser]
    queryset = QuestionsOfTheDay.objects.all()
    serializer_class = QuestionsOfTheDaySerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="qotd",
        permission_classes=[DjangoModelPermissions],
    )
    def get_qotd(self, request):
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
        permission_classes=[DjangoModelPermissions],
    )
    def generate_qotd(self, request):
        """
        Generate Questions of the Day.
        """
        try:
            number_of_questions = random.randint(8, 12)

            _ = QuestionsOfTheDay.objects.create(
                number_of_questions=number_of_questions
            )

            return Response(
                {"message": "Questions of the Day generated successfully"}, status=201
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)
