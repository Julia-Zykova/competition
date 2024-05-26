from rest_framework import generics, status
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
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get(self, request, *args, **kwargs):
        return self.index(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def index(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            ListPhotoService, request.GET.dict() | {
                'user': request.user if self.request.user.is_authenticated else None
            })
        queryset = self.paginate_queryset(outcome.result)
        serializer = PhotoSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            UploadPhotoService, self.request.POST.dict() | {
                'author': self.request.user if self.request.user.is_authenticated else None
            }, self.request.FILES.dict()
        )
        return Response(PhotoSerializer(outcome.result).data, status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #     author = get_object_or_404(CustomUser, id=self.request.user.id)
    #     return serializer.save(author=author)


class RetrieveUpdateDestroyPhotoAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    permission_classes = [IsOwnerOrReadOnly,]
    http_method_names = ['get', 'head', 'options', 'patch', 'delete']

    def get(self, request, *args, **kwargs):
        return self.index(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def index(self, request, *args, **kwargs):
        outcome = ServiceOutcome(DetailPhotoService, request.GET.dict() | {"photo": self.kwargs["pk"]})
        photo_serializer = PhotoSerializer(outcome.result['photo'])
        comment_serializer = CommentSerializer(outcome.result['comments'], many=True)
        return Response(
            {'photo': photo_serializer.data, 'comments': comment_serializer.data}, status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            EditPhotoService, request.POST.dict() | {'photo': self.kwargs['pk']})
        serializer = PhotoSerializer(outcome.result)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            SoftDeletePhotoService, request.POST.dict() | {'photo': self.kwargs['pk']})
        serializer = PhotoSerializer(outcome.result)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class UpdatePhotoRestoreAPIView(generics.UpdateAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    permission_classes = [IsOwnerOrReadOnly,]

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            RestorePhotoService, request.POST.dict() | {'photo': self.kwargs['pk']})
        serializer = PhotoSerializer(outcome.result)
        return Response(serializer.data, status=status.HTTP_200_OK)
