from django.shortcuts import render, redirect

from django.views.generic import View
from service_objects.services import ServiceOutcome

from models_app.models import Photo
from models_app.models.photo.forms import UploadPhotoForm

from photo_app.services.photo.edit import EditPhotoService


class EditPhotoView(View):
    template_name = 'photo_app/edit_photo.html'
    #permission_classes = (IsAuthenticated)
    
    def get(self, request, *args, **kwargs):
        #import pdb
        #pdb.set_trace()
        return render(
            request, self.template_name,
            context = {'photo': Photo.objects.get(id=self.kwargs['id'])})
    
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            EditPhotoService, request.POST.dict() | {'photo':self.kwargs['id']})
        return redirect('photo_app:home')
