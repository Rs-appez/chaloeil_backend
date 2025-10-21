from django.db import models
from django.db.models import QuerySet, Sum
from question.models import Answer, Question, QuestionsOfTheDay


class Participant(models.Model):
    def is_player(self) -> bool:
        """
        Checks if the participant is a Player.
        """
        return hasattr(self, "player")

    def is_team(self) -> bool:
        """
        Checks if the participant is a Team.
        """
        return hasattr(self, "team")

    def get_real_instance(self):
        """
        Returns the real instance of the participant, which can be either a Player or a Team.
        """
        if hasattr(self, "player"):
            return self.player
        elif hasattr(self, "team"):
            return self.team
        return self  # Fallback to Participant

    def __str__(self) -> str:
        return f"{self.get_real_instance()}"


class Player(Participant):
    discord_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name} - ({self.discord_id})"


class TeamName(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Team(Participant):
    players = models.ManyToManyField(Player, related_name="teams")
    names = models.ManyToManyField(TeamName, related_name="teams")

    def __str__(self) -> str:
        return f"Team with {[', '.join(player.name for player in self.players.all())]}"

    @staticmethod
    def get_team_by_players(players):
        """
        Returns a team that contains all the players with the given IDs.
        If no such team exists, returns None.
        """
        players = Player.objects.filter(discord_id__in=players)
        player_ids = set(p.id for p in players)
        for team in Team.objects.annotate(num_players=models.Count("players")).filter(
            num_players=len(player_ids)
        ):
            team_player_ids = set(team.players.values_list("id", flat=True))
            if team_player_ids == player_ids:
                return team

        return None

    def add_name(self, name: str):
        """
        Adds a name to the team.
        If the name already exists, it will not be added again.
        """
        team_name, created = TeamName.objects.get_or_create(name=name)
        self.names.add(team_name)
        return team_name


class AnswerSelected(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    number_of_times = models.PositiveIntegerField(default=0)


class Statistic(models.Model):
    player = models.ForeignKey(
        Participant, on_delete=models.SET_NULL, null=True, blank=True
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    asked_count = models.PositiveIntegerField(default=0)
    correct_count = models.PositiveIntegerField(default=0)
    incorrect_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"Statistics for {self.player} on {self.question.question_text}"

    def increment_asked_count(self, answer: Answer):
        self.asked_count += 1

        if answer:
            if answer.is_correct:
                self.correct_count += 1
            else:
                self.incorrect_count += 1

            answer_selected, created = AnswerSelected.objects.get_or_create(
                answer=answer
            )
            answer_selected.number_of_times += 1
            answer_selected.save()

        self.save()

    @staticmethod
    def get_pourcentage(
        stats: QuerySet["Statistic"],
    ) -> list[dict[str, object]]:
        aggregated = stats.values(
            "question",
        ).annotate(total_correct=Sum("correct_count"), total_asked=Sum("asked_count"))

        question_ids = {stat["question"] for stat in aggregated}
        questions_map = {q.id: q for q in Question.objects.filter(id__in=question_ids)}
        results = [
            {
                "question": questions_map[stat["question"]].question_text,
                "percentage": (
                    stat["total_correct"] / stat["total_asked"] * 100.0
                    if stat["total_asked"]
                    else 0.0
                ),
                "image": questions_map[stat["question"]].get_image_url(),
                "level": questions_map[stat["question"]].level.level_text,
            }
            for stat in aggregated
        ]

        return sorted(results, key=lambda item: item["percentage"], reverse=True)


class PlayerQotd(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    question_of_the_day = models.ForeignKey(QuestionsOfTheDay, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("player", "question_of_the_day")

    def __str__(self) -> str:
        return f"{self.player} - QOTD: {self.question_of_the_day}"


class QotdStatistic(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.player} - Score: {self.score}"

    def increment_score(self, points: int):
        self.score += points
        self.save()
