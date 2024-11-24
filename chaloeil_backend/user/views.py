from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import UserBot
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = UserBot.objects.all()
    serializer_class = UserSerializer
    
