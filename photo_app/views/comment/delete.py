from django.shortcuts import render, redirect

from django.views.generic import View
from service_objects.services import ServiceOutcome

from photo_app.services.comment.delete import DeleteCommentService


class DeleteCommentView(View):
    
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            DeleteCommentService, request.POST.dict() | {'photo':self.kwargs['id']})
        return redirect('photo_app:home')
