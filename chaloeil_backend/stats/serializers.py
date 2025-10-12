from rest_framework import serializers

from .models import (
    Player,
    Team,
    Statistic,
    AnswerSelected,
    TeamName,
    Participant,
    QotdStatistic,
)
from question.serializers import QuestionSerializer, AnswerSerializer


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "discord_id", "name"]


class TeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamName
        fields = ["name"]


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    names = TeamNameSerializer(many=True)

    class Meta:
        model = Team
        fields = ["id", "players", "names"]


class AnswerSelectedSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer()

    class Meta:
        model = AnswerSelected
        fields = ["answer", "number_of_times"]


class ParticipantSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        if instance.is_player():
            return PlayerSerializer(instance.get_real_instance()).data
        elif instance.is_team():
            return TeamSerializer(instance.get_real_instance()).data
        return super().to_representation(instance)

    class Meta:
        model = Participant
        fields = ["id"]


class StatisticsSerializer(serializers.ModelSerializer):
    player = ParticipantSerializer()
    question = QuestionSerializer()
    answers = AnswerSelectedSerializer(many=True)

    class Meta:
        model = Statistic
        fields = [
            "id",
            "player",
            "question",
            "asked_count",
            "correct_count",
            "incorrect_count",
            "answers",
        ]


class QotdStatisticSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()

    class Meta:
        model = QotdStatistic
        fields = ["id", "player", "score"]
