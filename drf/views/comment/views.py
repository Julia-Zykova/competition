from rest_framework import generics, status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.response import Response
from service_objects.services import ServiceOutcome

from drf.permissions import IsOwnerOrReadOnly
from drf.serializers import CommentRetrieveSerializer, CommentSerializer, CommentListSerializer
from drf.services import ListCommentsService, CreateCommentService, DestroyCommentService, PatchCommentService, \
    RetrieveCommentService

from drf.utils import LargeCommentsPagination
from models_app.models import Comment


class ListCreateCommentsAPIView(generics.ListCreateAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()
    pagination_class = LargeCommentsPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            ListCommentsService, request.GET.dict() | {
                "photo": self.kwargs["photo"],
            })
        queryset = self.paginate_queryset(outcome.result)
        serializer = CommentListSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            CreateCommentService, self.request.POST.dict() | {
                "user": self.request.user if self.request.user.is_authenticated else None
            }
        )
        return Response(CommentListSerializer(outcome.result).data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyCommentAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentRetrieveSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly, ]
    http_method_names = ["get", "head", "options", "patch", "delete"]

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(RetrieveCommentService, request.GET.dict() | {
            "comment": self.kwargs["comment"],
        })

        return Response(
            {
                "comment": CommentRetrieveSerializer(outcome.result["comment"]).data,
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            DestroyCommentService, request.data | {"comment": self.kwargs["comment"]})
        return Response(CommentSerializer(outcome.result).data, status=status.HTTP_204_NO_CONTENT)

    @parser_classes([JSONParser])
    def patch(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            PatchCommentService, request.data | {"comment": self.kwargs["comment"]})
        return Response(CommentSerializer(outcome.result).data, status=status.HTTP_200_OK)
