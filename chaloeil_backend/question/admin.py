from django.contrib import admin

from .models import (
    Answer,
    Category,
    Question,
    Level,
    QuestionsOfTheDay,
    QuestionsOfTheDayQuestion,
)

admin.site.register(Category)
admin.site.register(Level)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    class AnswerInline(admin.TabularInline):
        model = Answer
        extra = 4

    inlines = [AnswerInline]
    save_as = True
    list_display = ("question_text", "display_categories", "level")
    list_filter = ["categories", "level"]
    search_fields = ["question_text"]

    def display_categories(self, obj):
        return ", ".join([category.category_text for category in obj.categories.all()])

    display_categories.short_description = "Categories"


@admin.register(QuestionsOfTheDay)
class QuestionsOfTheDayAdmin(admin.ModelAdmin):
    class QuestionsOfTheDayQuestionInline(admin.TabularInline):
        model = QuestionsOfTheDayQuestion
        extra = 0
        readonly_fields = ["order"]
        ordering = ("order",)

    inlines = [QuestionsOfTheDayQuestionInline]

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields + ("number_of_questions",)
        return self.readonly_fields
