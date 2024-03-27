from django.shortcuts import render, redirect

from django.views.generic import View
from service_objects.services import ServiceOutcome

from photo_app.services.photo.soft_delete import SoftDeletePhotoService


class DeletePhotoView(View):
    #permission_classes = (IsAuthenticated)
    
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            SoftDeletePhotoService, request.POST.dict() | {'photo':self.kwargs['id']})
        return redirect('photo_app:home')
