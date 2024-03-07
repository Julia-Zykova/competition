from django.shortcuts import render, redirect

from service_objects.views import ServiceView
from photo_app.services.upload_photo import UploadPhotoService
from models_app.models.photo.forms import UploadPhotoForm

class UploadPhotoView(ServiceView):
    form_class = UploadPhotoForm
    service_class = UploadPhotoService
    template_name = 'photo_app/upload_photos.html'
    #success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = UploadPhotoForm()
            context = {"form":form}
            return render(request, self.template_name, context)

    def post(self, request):

        if request.method == 'POST':
            form = UploadPhotoForm(request.POST,request.FILES)
            if form.is_valid():

                post = form.save(commit=False)
                form.save()
            
            return redirect('upload')