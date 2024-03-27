from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.generic import View
from service_objects.services import ServiceOutcome
from photo_app.services.photo.upload import UploadPhotoService
from models_app.models.photo.forms import UploadPhotoForm

class UploadPhotoView(View):   
    template_name = 'photo_app/upload_photos.html'
    #permission_classes = (IsAuthenticated)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context = {"form":UploadPhotoForm()})

    
    def post(self, request):
        user = request.user
        if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
            if user._wrapped.__class__ == object:
                user._setup()
            user = user._wrapped

        outcome = ServiceOutcome(
            UploadPhotoService, request.POST.dict() | {'author': request.user}, request.FILES.dict()
            )
        #import pdb
        #pdb.set_trace()
        return redirect('photo_app:home')