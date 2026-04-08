from rest_framework import serializers
from .models import AlmanaxEntry, EconomyEntry


class AlmanaxEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AlmanaxEntry
        fields = "__all__"


class EconomyEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EconomyEntry
        fields = "__all__"
