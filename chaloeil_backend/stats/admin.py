from django.contrib import admin

from . import models as m

admin.site.register(m.Player)
admin.site.register(m.Team)
admin.site.register(m.Statistic)
admin.site.register(m.AnswerSelected)
admin.site.register(m.Participant)
admin.site.register(m.TeamName)
admin.site.register(m.QotdStatistic)
