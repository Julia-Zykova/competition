from django.views.generic import View
from django.shortcuts import render

from models_app.models.photo.models import Photo
from models_app.models.user.models import CustomUser


class PersonalAccountView(View):
   #permission_classes = (IsAuthenticated)

    def get_queryset(self):
        return CustomUser.objects.get(id = self.kwargs['id'])

    def get(self, request, **kwargs):
        return render(
            request, template_name='photo_app/personal_account.html',
            context = {'user': self.get_queryset(),
            'photo': Photo.objects.filter(author=self.kwargs['id'])[:4]}
            )
    
    #def post(self, request, **kwargs):
    #    user = request.user
            
    #    if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
    #        if user._wrapped.__class__ == object:
    #            user._setup()
    #        user = user._wrapped

    #    outcome = ServiceOutcome(
    #        CommentForPhotoService, request.POST.dict() |
    #        {'user': request.user, 'photo':self.kwargs['id']})
    #    return redirect('photo_app:home')