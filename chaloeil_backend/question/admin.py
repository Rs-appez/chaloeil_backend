from django.contrib import admin

from .models import Answer, Category, Question , Level

class AnswerInline(admin.TabularInline):
  model = Answer
  extra = 4

class QuestionAdmin(admin.ModelAdmin):
  inlines = [AnswerInline]  
  save_as = True
  list_display = ('question_text', 'display_categories', 'level')
  list_filter = ['categories','level']
  search_fields = ['question_text']

  def display_categories(self, obj):
    return ", ".join([category.category_text for category in obj.categories.all()])
  display_categories.short_description = 'Categories'

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Category)
admin.site.register(Level)