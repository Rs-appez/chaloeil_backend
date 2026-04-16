import json

from django.db.utils import IntegrityError
from django.utils import timezone
from question.models import Answer, Question, QuestionOfTheDaySession, QuestionsOfTheDay
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from .models import (
    Player,
    PlayerQotd,
    QotdStatistic,
    SessionStatistic,
    Statistic,
    Team,
)
from .serializers import (
    PlayerSerializer,
    SessionStatisticSerializer,
    StatisticsSerializer,
    TeamSerializer,
)


class StatisticsViewSet(viewsets.GenericViewSet):
    """
    ViewSet for handling statistics related to players and questions.
    """

    queryset = Statistic.objects.all()
    serializer_class = StatisticsSerializer
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=["post"], permission_classes=[DjangoModelPermissions])
    def add_answer(self, request):
        try:
            question_id = request.data.get("question_id")
            answers = json.loads(request.data.get("answers"))
            for data in answers:
                player = data.get("player_id", None)
                players = data.get("players_id", None)
                team = None

                answer_id = data.get("answer_id")

                if player:
                    player = Player.objects.get(discord_id=player)
                    if not player:
                        return Response({"error": "Player not found"}, status=404)

                elif players:
                    team = Team.get_team_by_players(players)
                    if not team:
                        return Response({"error": "Team not found"}, status=404)
                else:
                    return Response(
                        {"error": "Either player_id or players_id must be provided"},
                        status=400,
                    )

                participant = player or team

                question = Question.objects.get(id=question_id)
                if not question:
                    return Response({"error": "Question not found"}, status=404)
                answer = Answer.objects.filter(id=answer_id).first()

                statistics, _ = Statistic.objects.get_or_create(
                    player=participant, question=question
                )

                if answer:
                    statistics.increment_asked_count(answer)

            return Response("Statistics added successfully", status=201)

        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=400)


class PlayerViewSet(viewsets.GenericViewSet):
    """
    ViewSet for handling player-related operations.
    """

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=["post"], permission_classes=[DjangoModelPermissions])
    def add_players(self, request):
        """
        Adds players to the database from a JSON payload.
        """
        try:
            players_data = json.loads(request.data.get("players", "[]"))
            for player_data in players_data:
                player, created = Player.objects.get_or_create(
                    discord_id=player_data["discord_id"],
                    defaults={"name": player_data["name"]},
                )
                if not created and player.name != player_data["name"]:
                    player.name = player_data["name"]
                    player.save()
            return Response("Players added successfully", status=201)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format"}, status=400)


class TeamViewSet(viewsets.GenericViewSet):
    """
    ViewSet for handling team-related operations.
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=["post"], permission_classes=[DjangoModelPermissions])
    def add_teams(self, request):
        """
        Adds teams to the database from a JSON payload.
        """
        try:
            teams_data = json.loads(request.data.get("teams", "[]"))
            for team_data in teams_data:
                team = Team.get_team_by_players(team_data["players"])
                if not team:
                    team = Team.objects.create()
                    players = []
                    for player_id in team_data["players"]:
                        player, _ = Player.objects.get_or_create(discord_id=player_id)
                        players.append(player)
                    team.players.set(players)

                _ = team.add_name(team_data["name"])
                team.save()
            return Response("Teams added successfully", status=201)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format"}, status=400)


class QotdStatisticViewSet(viewsets.GenericViewSet):
    """
    ViewSet for handling Questions of the Day statistics.
    """

    queryset = QotdStatistic.objects.all()
    serializer_class = StatisticsSerializer
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=["post"], permission_classes=[DjangoModelPermissions])
    def add_score(self, request):
        try:
            player_id = str(request.data.get("player_id"))

            try:
                score = int(request.data.get("score", 0))
            except ValueError:
                return Response({"error": "Score must be an integer"}, status=400)

            player, _ = Player.objects.get_or_create(discord_id=player_id)

            qotd_statistic, _ = QotdStatistic.objects.get_or_create(
                player=player,
            )

            qotd_statistic.increment_score(score)

            return Response("QotdStatistic updated successfully", status=200)
        except TypeError as e:
            return Response({"error": f"Invalid data type: {str(e)}"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @action(detail=False, methods=["post"], permission_classes=[DjangoModelPermissions])
    def log_player(self, request):
        try:
            player_id = str(request.data.get("player_id"))
            question_of_the_day_id = int(request.data.get("qotd_id"))

            player, _ = Player.objects.get_or_create(discord_id=player_id)

            question_of_the_day = QuestionsOfTheDay.objects.get(
                id=question_of_the_day_id
            )
            _ = PlayerQotd.objects.create(
                player=player, question_of_the_day=question_of_the_day
            )

            return Response("Player succefuly log", status=201)
        except TypeError as e:
            return Response({"error": f"Invalid data type: {str(e)}"}, status=400)
        except IntegrityError:
            return Response(
                {"error": "Player has already logged this QOTD"}, status=403
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class SessionStatisticViewSet(viewsets.GenericViewSet):
    """
    ViewSet for handling session statistics.
    """

    queryset = SessionStatistic.objects.all()
    serializer_class = SessionStatisticSerializer
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=["post"], permission_classes=[DjangoModelPermissions])
    def add_score(self, request):
        try:
            player_id = str(request.data.get("player_id"))
            try:
                score = int(request.data.get("score", 0))
            except ValueError:
                return Response({"error": "Score must be an integer"}, status=400)

            player, _ = Player.objects.get_or_create(discord_id=player_id)
            session = (
                QuestionOfTheDaySession.objects.filter(
                    active=True, date__lt=timezone.now()
                )
                .only("id")
                .last()
            )

            if not session:
                return Response({"error": "No active session found"}, status=404)

            stat, _ = SessionStatistic.objects.get_or_create(
                player=player, session=session, defaults={"score": 0}
            )
            stat.increment_score(score)

            return Response("SessionStatistic updated successfully", status=200)
        except TypeError as e:
            return Response({"error": f"Invalid data type: {str(e)}"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
