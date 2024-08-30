from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from service_objects.services import ServiceOutcome

from drf.permissions import IsOwnerOrReadOnly
from drf.serializers import (
    CommentListSerializer,
    CommentRetrieveSerializer,
    CommentSerializer,
    CreateCommentSerializer,
)
from drf.services import (
    CreateCommentService,
    DestroyCommentService,
    ListCommentsService,
    PatchCommentService,
    RetrieveCommentService,
)
from models_app.models import Comment
from utils.pagination import LargeCommentsPagination


class ListCreateCommentsAPIView(generics.ListCreateAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()
    pagination_class = LargeCommentsPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "photo",
                openapi.IN_PATH,
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            "200": openapi.Response("OK", schema=CommentListSerializer(many=True)),
            "400": "Invalid parameters",
        },
        operation_description="Shows a list of comments on a photo using a set of parameters: page size, page number",
    )
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            ListCommentsService,
            request.GET.dict()
            | {
                "photo": self.kwargs["photo"],
            },
        )
        queryset = self.paginate_queryset(outcome.result)
        serializer = CommentListSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=CreateCommentSerializer,
        responses={
            "201": openapi.Response(description="Comment was create successfully", schema=CommentListSerializer),
            "400": "Invalid parameters",
            "401": "Unauthorized",
        },
        operation_description="Adds a comment to the photo",
    )
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            CreateCommentService,
            self.request.POST.dict() | {"user": self.request.user if self.request.user.is_authenticated else None},
        )
        return Response(CommentListSerializer(outcome.result).data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyCommentAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentRetrieveSerializer
    queryset = Comment.objects.all()
    permission_classes = [
        IsOwnerOrReadOnly,
    ]
    http_method_names = ["get", "head", "options", "patch", "delete"]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "photo",
                openapi.IN_PATH,
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            "200": openapi.Response("OK", schema=CommentRetrieveSerializer),
            "400": "Invalid parameter 'comment'",
        },
        operation_description="Shows a list of answers on a comment",
    )
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            RetrieveCommentService,
            request.GET.dict()
            | {
                "comment": self.kwargs["comment"],
            },
        )

        return Response(
            {
                "comment": CommentRetrieveSerializer(outcome.result).data,
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={
            "201": openapi.Response("Comment was mark as deleted successfully", schema=CommentSerializer),
            "400": "Invalid parameter 'comment'",
            "401": "Unauthorized or insufficient permissions to access",
        },
        operation_description="Deletes the user's comment",
    )
    def delete(self, request, *args, **kwargs):
        outcome = ServiceOutcome(DestroyCommentService, request.data | {"comment": self.kwargs["comment"]})
        return Response(CommentSerializer(outcome.result).data, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={
            "200": openapi.Response("Comment's text was changed successfully", schema=CommentSerializer),
            "400": "Invalid parameter 'comment'",
            "401": "Unauthorized or insufficient permissions to access",
        },
        operation_description="Changes the text of comment",
    )
    @parser_classes([JSONParser])
    def patch(self, request, *args, **kwargs):
        outcome = ServiceOutcome(PatchCommentService, request.data | {"comment": self.kwargs["comment"]})
        return Response(CommentSerializer(outcome.result).data, status=status.HTTP_200_OK)
