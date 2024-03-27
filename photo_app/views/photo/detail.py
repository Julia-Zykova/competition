from django.views.generic import View
from django.shortcuts import render, redirect

from service_objects.services import ServiceOutcome

from photo_app.services.comment.comment_for_photo import CommentForPhotoService

from models_app.models.photo.models import Photo
from models_app.models.comment.models import Comment


class DetailPhotoView(View):
    #permission_classes = (IsAuthenticatedOrReadOnly) 

    def get_queryset(self):
        return Photo.objects.get(id = self.kwargs['id'])

    def get(self, request, **kwargs):
        return render(
            request, template_name='photo_app/detail_photo.html',
            context = {'photo': self.get_queryset(),
            'comments': Comment.objects.filter(photo=self.get_queryset()).order_by('-created_at')[:3]}
            )
    
    def post(self, request, **kwargs):
        user = request.user
            
        if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
            if user._wrapped.__class__ == object:
                user._setup()
            user = user._wrapped

        outcome = ServiceOutcome(
            CommentForPhotoService, request.POST.dict() |
            {'user': request.user, 'photo':self.kwargs['id']})
        return redirect('photo_app:home')
        
        