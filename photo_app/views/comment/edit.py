from django.shortcuts import render, redirect

from django.views.generic import View
from service_objects.services import ServiceOutcome

from models_app.models import Comment

from photo_app.services.comment.edit import EditCommentService


class EditCommentView(View):
    #permission_classes = (IsAuthenticated)
    
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            EditCommentService, request.POST.dict())
        return redirect('photo_app:detail')
