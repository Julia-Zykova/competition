from rest_framework import generics, status
from rest_framework.response import Response

from drf.permissions import IsOwnerOrReadOnly
from drf.serializers import VoiceSerializer
from drf.services import CreateVoiceService, DestroyVoiceService
from models_app.models import Voice

from service_objects.services import ServiceOutcome

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CreateVoiceAPIView(generics.CreateAPIView):
    serializer_class = VoiceSerializer
    queryset = Voice.objects.all()
    permission_classes = [IsOwnerOrReadOnly, ]

    @swagger_auto_schema(
        request_body=VoiceSerializer,
        operation_description="Adds a voice to the photo. One user can vote for one photo once"
    )
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            CreateVoiceService, request.POST.dict() | {
                "user": request.user if self.request.user.is_authenticated else None,
                "photo": self.kwargs["photo"],

            })
        return Response(VoiceSerializer(outcome.result).data, status=status.HTTP_201_CREATED)


class DestroyVoiceAPIView(generics.DestroyAPIView):
    serializer_class = VoiceSerializer
    queryset = Voice.objects.all()
    permission_classes = [IsOwnerOrReadOnly, ]

    @swagger_auto_schema(
        request_body=VoiceSerializer,
        operation_description="Removes the voice from the photo"
    )
    def delete(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            DestroyVoiceService, request.POST.dict() | {
                "user": request.user if self.request.user.is_authenticated else None,
                "photo": self.kwargs["photo"],

            })
        return Response(VoiceSerializer(outcome.result).data, status=status.HTTP_204_NO_CONTENT)
