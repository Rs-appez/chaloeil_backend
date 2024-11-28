from django.contrib import admin

from .models import Word

class WordAdmin(admin.ModelAdmin):
    list_editable = ['word']

admin.site.register(Word)