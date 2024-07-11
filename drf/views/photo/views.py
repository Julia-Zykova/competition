from rest_framework import generics, status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from service_objects.services import ServiceOutcome

from drf.permissions import IsOwnerOrReadOnly
from drf.schemas import list_photos, invalid_inputs
from drf.services import ListPhotoService, DetailPhotoService, EditPhotoService, UploadPhotoService, \
    SoftDeletePhotoService
from drf.services.photo.restore import RestorePhotoService
from utils.pagination import PhotoPagination
from models_app.models import Photo
from drf.serializers import PhotoSerializer, CommentSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ListCreatePhotosAPIView(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    pagination_class = PhotoPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'orderby', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING,
                description="Photos will be sorted by this parameter.",
                enum=['pub_date', '-pub_date', 'voices', '-voices', 'comments', '-comments']
            ),
            openapi.Parameter(
                'orderbysearch', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING,
                description="Search by photo title, photo author(email),description"
            ),
            openapi.Parameter(
                'personal_list', openapi.IN_QUERY, required=False, type=openapi.TYPE_BOOLEAN,
                description="Display only the photos that the user uploaded or all photos"
            ),
            openapi.Parameter(
                'personal_filter', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING,
                description="Filters user photos by moderation status.",
                enum=["in_moderation", "approved", "on_delete"]
            ),
        ],
        responses={
            "200": openapi.Response("OK", schema=list_photos),
            "400": openapi.Response("Invalid parameters", schema=invalid_inputs),
        },
        operation_description="Shows a list of photos using a set of parameters: page size, page number, sort by, "
                              "search, personal photos and filter personal photos by moderation state",
    )
    def get(self, request: HttpRequest, *args, **kwargs) -> 'HttpResponse':
        outcome = ServiceOutcome(
            ListPhotoService, request.GET.dict() | {
                "user": request.user if self.request.user.is_authenticated else None
            })
        queryset = self.paginate_queryset(outcome.result)
        serializer = PhotoSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=PhotoSerializer,
                         responses={
                             "201": openapi.Response("Photo was upload successfully", schema=PhotoSerializer),
                             "400": "Invalid parameters",
                             "401": "Unauthorized",
                         },
                         operation_description="Uploading photos")
    def post(self, request: HttpRequest, *args, **kwargs) -> 'HttpResponse':
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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'com_size', openapi.IN_QUERY, required=False, type=openapi.TYPE_INTEGER,
                description="Number of comments results to return per page."
            ),
            openapi.Parameter(
                'photo', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            "200": openapi.Response("OK", schema=PhotoSerializer),
            "400": "Invalid parameters",
        },
        operation_description="View the photo in detail with comments on it. The number of comments might be changed "
                              "using the 'com_size' parameter, by default there it's 3."
    )
    def get(self, request: HttpRequest, *args, **kwargs) -> 'HttpResponse':
        outcome = ServiceOutcome(DetailPhotoService, request.GET.dict() | {
            "photo": self.kwargs["photo"],
            "user": request.user.id if self.request.user.is_authenticated else None,
            "com_size": int(request.query_params["com_size"]) if request.query_params else None,
        })
        photo_serializer = PhotoSerializer(outcome.result["photo"])
        comment_serializer = CommentSerializer(outcome.result["comments"], many=True)
        return Response(
            {"photo": photo_serializer.data, "comments": comment_serializer.data}, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=PhotoSerializer,
                         responses={
                             "204": openapi.Response("Photo was marked as deleted successfully",
                                                     schema=PhotoSerializer),
                             "400": "Invalid parameters",
                             "401": "Unauthorized or insufficient permissions to access",
                         },
                         operation_description="Sets the 'is_deleted' parameter to True"
                         )
    def delete(self, request: HttpRequest, *args, **kwargs) -> 'HttpResponse':
        outcome = ServiceOutcome(
            SoftDeletePhotoService, request.data | {"photo": self.kwargs["photo"]})
        serializer = PhotoSerializer(outcome.result)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=PhotoSerializer,
        responses={
            "200": openapi.Response("Data was change successfully", schema=PhotoSerializer),
            "400": "Invalid parameters",
            "401": "Unauthorized or insufficient permissions to access",
        },
        operation_description="Changes the title and/or description of the photo"
    )
    @parser_classes([JSONParser])
    def patch(self, request: HttpRequest, *args, **kwargs) -> 'HttpResponse':
        outcome = ServiceOutcome(
            EditPhotoService, request.data | {"photo": self.kwargs["photo"]})
        serializer = PhotoSerializer(outcome.result)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatePhotoRestoreAPIView(generics.UpdateAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    permission_classes = [IsOwnerOrReadOnly, ]
    http_method_names = ["patch", ]

    @swagger_auto_schema(request_body=PhotoSerializer,
                         responses={
                             "200": openapi.Response("State was change successfully", schema=PhotoSerializer),
                             "400": "Invalid parameters",
                             "401": "Unauthorized or insufficient permissions to access",
                         },
                         operation_description="Sets the 'is_deleted' parameter to False")
    def patch(self, request: HttpRequest, *args, **kwargs) -> 'HttpResponse':
        outcome = ServiceOutcome(
            RestorePhotoService, request.data | {"photo": self.kwargs["photo"]})
        serializer = PhotoSerializer(outcome.result)
        return Response(serializer.data, status=status.HTTP_200_OK)
