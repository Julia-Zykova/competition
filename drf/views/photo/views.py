from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from service_objects.services import ServiceOutcome

from drf.services.photo.list import ListPhotoService
from models_app.models import Photo, CustomUser
from photo_app.serializers import PhotoSerializer
from photo_app.services import UploadPhotoService


class ListCreatePhotosAPIView(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()

    def get(self, request, *args, **kwargs):
        return self.index(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def index(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            ListPhotoService, request.GET.dict() | {
                'user': request.user if self.request.user.is_authenticated else None
            })

        queryset = outcome.result
        serializer = PhotoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            UploadPhotoService, self.request.POST.dict() | {
                'author': self.request.user if self.request.user.is_authenticated else None
            }, self.request.FILES.dict()
        )
        return Response(PhotoSerializer(outcome.result).data)

    # def perform_create(self, serializer):
    #     author = get_object_or_404(CustomUser, id=self.request.user.id)
    #     return serializer.save(author=author)

