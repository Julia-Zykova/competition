from django.shortcuts import render, redirect

from django.views.generic import View
from service_objects.services import ServiceOutcome
from photo_app.services.upload_photo import UploadPhotoService
from models_app.models.photo.forms import UploadPhotoForm

class UploadPhotoView(View):   
    template_name = 'photo_app/upload_photos.html'

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = UploadPhotoForm()
            context = {"form":form}
            return render(request, self.template_name, context)

    
    def post(self, request):
        user = request.user
        if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
            if user._wrapped.__class__ == object:
                user._setup()
            user = user._wrapped
        outcome = ServiceOutcome(
            UploadPhotoService, request.POST.dict() | {'author': request.user}, request.FILES.dict()
            )
        return redirect('upload')