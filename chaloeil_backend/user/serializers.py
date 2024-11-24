from .models import UserBot
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBot
        fields = ['username','discord_id']