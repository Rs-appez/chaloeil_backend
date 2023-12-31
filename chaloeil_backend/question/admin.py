from django.contrib import admin

from .models import Answer, Category, Question , Level

class AnswerInline(admin.TabularInline):
  model = Answer
  extra = 4

class QuestionAdmin(admin.ModelAdmin):
  inlines = [AnswerInline]

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Category)
admin.site.register(Level)