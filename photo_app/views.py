import json
import datetime as dt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from service_objects.views import ServiceView
from asgiref.sync import sync_to_async

from .services.upload_photo import UploadPhotoService
from models_app.models.photo.forms import UploadPhotoForm
from models_app.models.photo.models import Photo
from models_app.models.user.models import CustomUser
from models_app.models.voice.models import Voice



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
            


def datetime_to_str(self):
    import datetime
    str_datetime = self.strftime('%j.%m.%Y  %H:%i')


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

        #Получаем словарь из queryset
        q_val = qs.values()
        #Формируем новый словарь, состоящий из ключа "title" и всех значений      
        q_dict = dict()
        #Перебираем словарь queryset, чтобы получить отдельно "title" и обновляем словарь q_dict 
        for q in q_val.values():
            q_tmp_dict = dict()
            q_tmp_dict[q['title']] = q
            q_dict.update(q_tmp_dict)
            

                          
        return JsonResponse(q_dict, safe=False)




class DetailPhotoView(DetailView):
    model = Photo
    template_name = 'photo_app/detail_photo.html'
    pk_url_kwarg = 'photo_id'
    context_object_name = 'photo'

    

