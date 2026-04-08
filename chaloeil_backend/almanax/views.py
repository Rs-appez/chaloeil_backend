from rest_framework import viewsets
from .models import AlmanaxEntry, EconomyEntry
from .serializers import AlmanaxEntrySerializer, EconomyEntrySerializer


class EconomyEntryViewSet(viewsets.ModelViewSet):
    queryset = EconomyEntry.objects.all()
    serializer_class = EconomyEntrySerializer
