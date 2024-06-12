from rest_framework import generics, status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from service_objects.services import ServiceOutcome

from drf.permissions import IsOwnerOrReadOnly
from drf.services import ListPhotoService, DetailPhotoService, EditPhotoService, UploadPhotoService, \
    SoftDeletePhotoService
from drf.services.photo.restore import RestorePhotoService
from drf.utils import PhotoPagination
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
                description="Photos will be sorted by this parameter.\n"
                            "Available options:\n"
                            "pub_date, -pub_date, voices, -voices, comments, -comments."
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
                description="Filters user photos by moderation status. \n"
                            "Available options:\n"
                            "in_moderation, approved, on_delete."
            ),
        ],
        responses={
            "200": "OK",
            "400": "Invalid parameters",
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
                             "201": "Photo was upload successfully",
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
            "200": "OK",
            "400": "Invalid parameters",
        },
        operation_description="View the photo in detail with comments on it. The number of comments might be changed "
                              "using the 'com_size' parameter, by default there it's 3."
    )
    def get(self, request: HttpRequest, *args, **kwargs) -> 'HttpResponse':
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

    @swagger_auto_schema(request_body=PhotoSerializer,
                         responses={
                             "204": "Photo was marked as deleted successfully",
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
        # manual_parameters=[
        #     openapi.Parameter(
        #         'title', openapi.IN_BODY, required=False, type=openapi.TYPE_STRING,
        #         description="Change the title of the photo"
        #     ),
        #     openapi.Parameter(
        #         'description', openapi.IN_BODY, required=False, type=openapi.TYPE_STRING,
        #         description="Change the description of the photo"
        #     ),
        # ],
        responses={
            "200": "Data was change successfully",
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
                             "200": "State was change successfully",
                             "400": "Invalid parameters",
                             "401": "Unauthorized or insufficient permissions to access",
                         },
                         operation_description="Sets the 'is_deleted' parameter to False")
    def patch(self, request: HttpRequest, *args, **kwargs) -> 'HttpResponse':
        outcome = ServiceOutcome(
            RestorePhotoService, request.data | {"photo": self.kwargs["photo"]})
        serializer = PhotoSerializer(outcome.result)
        return Response(serializer.data, status=status.HTTP_200_OK)
