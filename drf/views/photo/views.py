from rest_framework import generics

from rest_framework.response import Response
from service_objects.services import ServiceOutcome


from drf.services import ListPhotoService, DetailPhotoService, EditPhotoService, UploadPhotoService, SoftDeletePhotoService
from drf.utils import PhotoPagination
from models_app.models import Photo
from drf.serializers import PhotoSerializer, CommentSerializer


class ListCreatePhotosAPIView(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    pagination_class = PhotoPagination

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
        return Response(PhotoSerializer(outcome.result).data)

    # def perform_create(self, serializer):
    #     author = get_object_or_404(CustomUser, id=self.request.user.id)
    #     return serializer.save(author=author)


class RetrieveUpdateDestroyPhotoAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()

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
        return Response({'photo': photo_serializer.data, 'comments': comment_serializer.data})

    def update(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            EditPhotoService, request.POST.dict() | {'photo': self.kwargs['pk']})
        serializer = PhotoSerializer(outcome.result)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            SoftDeletePhotoService, request.POST.dict() | {'photo': self.kwargs['pk']})
        serializer = PhotoSerializer(outcome.result)
        return Response(serializer.data)
