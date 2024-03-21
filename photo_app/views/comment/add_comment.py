from django.shortcuts import render, redirect

from django.views.generic import View
from service_objects.services import ServiceOutcome

from photo_app.services.comment.comment_for_photo import CommentForPhotoService


class AddCommentPhotoView(View):
    
    def post(self, request, *args, **kwargs):
        user = request.user
            
        if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
            if user._wrapped.__class__ == object:
                user._setup()
            user = user._wrapped
            
        outcome = ServiceOutcome(
            CommentForPhotoService, request.POST.dict() |
            {'user': request.user, 'photo':self.kwargs['id']})
        
