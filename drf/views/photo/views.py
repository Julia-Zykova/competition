from rest_framework import generics, status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.response import Response
from service_objects.services import ServiceOutcome

from drf.permissions import IsOwnerOrReadOnly
from drf.services import ListPhotoService, DetailPhotoService, EditPhotoService, UploadPhotoService, \
    SoftDeletePhotoService
from drf.services.photo.restore import RestorePhotoService
from drf.utils import PhotoPagination
from models_app.models import Photo
from drf.serializers import PhotoSerializer, CommentSerializer


class ListCreatePhotosAPIView(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    pagination_class = PhotoPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            ListPhotoService, request.GET.dict() | {
                "user": request.user if self.request.user.is_authenticated else None
            })
        queryset = self.paginate_queryset(outcome.result)
        serializer = PhotoSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            UploadPhotoService, self.request.POST.dict() | {
                "author": self.request.user if self.request.user.is_authenticated else None
            }, self.request.FILES.dict()
        )
        return Response(PhotoSerializer(outcome.result).data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyPhotoAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    permission_classes = [IsOwnerOrReadOnly, ]
    http_method_names = ["get", "head", "options", "patch", "delete"]

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(DetailPhotoService, request.GET.dict() | {
            "photo": self.kwargs["photo"],
            "user": request.user if self.request.user.is_authenticated else None,
            "com_size": int(request.query_params["com_size"]) if request.query_params else None,
        })
        photo_serializer = PhotoSerializer(outcome.result["photo"])
        comment_serializer = CommentSerializer(outcome.result["comments"], many=True)
        return Response(
            {"photo": photo_serializer.data, "comments": comment_serializer.data}, status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            SoftDeletePhotoService, request.data | {"photo": self.kwargs["photo"]})
        serializer = PhotoSerializer(outcome.result)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @parser_classes([JSONParser])
    def patch(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            EditPhotoService, request.data | {"photo": self.kwargs["photo"]})
        serializer = PhotoSerializer(outcome.result)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatePhotoRestoreAPIView(generics.UpdateAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    permission_classes = [IsOwnerOrReadOnly, ]

    def patch(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            RestorePhotoService, request.data | {"photo": self.kwargs["photo"]})
        serializer = PhotoSerializer(outcome.result)
        return Response(serializer.data, status=status.HTTP_200_OK)
