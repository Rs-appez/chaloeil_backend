from django.shortcuts import render

from .models import Word
from .serializers import WordSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class WordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Word.objects.all()
    serializer_class = WordSerializer
