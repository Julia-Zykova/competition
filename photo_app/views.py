from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from service_objects.views import ServiceView
from django.db.models import Count, Q

from .services.upload_photo import UploadPhotoService
from models_app.models.photo.forms import UploadPhotoForm
from models_app.models.photo.models import Photo
from models_app.models.user.models import CustomUser
from models_app.models.voice.models import Voice



class UploadPhotoView(ServiceView):
    form_class = UploadPhotoForm
    service_class = UploadPhotoService
    template_name = 'photo_app/upload_photo.html'
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
    template_name = 'photo_app/list_of_photos.html'
    paginate_by = 20

    
    def get_queryset(self):
        qs = Photo.objects.all()

        orderby = self.request.GET.get('orderby')

        if orderby == 'DateOld':
            qs = Photo.objects.all().order_by('pub_date')
            
        if orderby == 'DateNew':
            qs = Photo.objects.all().order_by('-pub_date')

        if orderby == 'Voices':
            qs = Photo.objects.all()\
            .annotate(sum_voices=Count('voices'))\
            .order_by('-sum_voices')

        if orderby == 'VoicesRev':
            qs = Photo.objects.all()\
            .annotate(sum_voices=Count('voices'))\
            .order_by('sum_voices')

        if orderby == 'Comments':
            qs = Photo.objects.all()\
            .annotate(sum_comments=Count('comments'))\
            .order_by('-sum_comments')

        if orderby == 'CommentsRev':
            qs = Photo.objects.all()\
            .annotate(sum_comments=Count('comments'))\
            .order_by('sum_comments')

        
        orderbysearch = self.request.GET.get('orderbysearch')

        if orderbysearch:

            qs = Photo.objects.filter(
                Q(title__icontains=orderbysearch) |
                Q(description__icontains=orderbysearch) |
                Q(author__email__icontains=orderbysearch)
                )

        return qs


class DetailPhotoView(DetailView):
    model = Photo
    template_name = 'photo_app/detail_photo.html'
    id_url_kwarg = 'photo_id'
