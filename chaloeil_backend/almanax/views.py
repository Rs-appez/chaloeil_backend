from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from .models import EconomyEntry, Job
from .serializers import EconomyEntrySerializer


class EconomyEntryViewSet(viewsets.ModelViewSet[EconomyEntry]):
    queryset = EconomyEntry.objects.all()
    serializer_class = EconomyEntrySerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["get"], permission_classes=[IsAdminUser])
    def get_job(self, request: Request) -> Response:
        job = request.query_params.get("job", "").strip().capitalize()
        if job not in [job.value for job in Job]:
            return Response({"error": "job parameter is invalid"}, status=400)
        try:
            entry = EconomyEntry.objects.get(job=job)
            serializer = EconomyEntrySerializer(entry)
            return Response(serializer.data)
        except EconomyEntry.DoesNotExist:
            return Response({"error": "Job not found"}, status=404)
