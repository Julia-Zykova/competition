from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from service_objects.views import ServiceView

from .services.upload_photo import UploadPhotoService
from models_app.models.photo.forms import UploadPhotoForm
from models_app.models.photo.models import Photo
from models_app.models.user.models import CustomUser
from models_app.models.voice.models import Voice



class UploadPhotoView(ServiceView):
    form_class = UploadPhotoForm
    service_class = UploadPhotoService
    template_name = 'mysite/index.html'
    #success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
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
            



class ListPhotoView(ListView):
    model = Photo
    context_object_name = 'posts'
    queryset =  Photo.objects.all()
    template_name = 'mysite/list.html'
    paginate_by = 20

    class Meta:
        ordering = ['-created_at']

    def get_ordering(self):
        ordering = self.request.GET.get('orderby')
        return ordering



