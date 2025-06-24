from django.contrib import admin

from .models import Player, Team, Statistic, AnswerSelected, Participant, TeamName

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Statistic)
admin.site.register(AnswerSelected)
admin.site.register(Participant)
admin.site.register(TeamName)
