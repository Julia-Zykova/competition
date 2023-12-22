from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from service_objects.views import ServiceView
from rest_framework.renderers import JSONRenderer

from .services.upload_photo import UploadPhotoService
from models_app.models.photo.forms import UploadPhotoForm
from models_app.models.photo.models import Photo
from models_app.models.user.models import CustomUser
from models_app.models.voice.models import Voice
from models_app.models.comment.models import Comment
from photo_app.serializers import PhotoSerializer



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
            

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class ListPhotoView(ListView):
    model = Photo
    context_object_name = 'posts'
    template_name = 'photo_app/list_of_photos.html'
    paginate_by = 12

        
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


    def get(self, request, *args, **kwargs):
        print("In view")
        qs = self.get_queryset()


        if request.method == 'GET' and is_ajax(request):
            print("Ajax")
            serialized_data = PhotoSerializer(qs, many = True).data
            
            
            q_dict = {"posts": serialized_data}              
            return JsonResponse(q_dict, safe=False)

        elif request.method == 'GET'and not is_ajax(request):
            context = {"posts": qs}
            
            return render(request,template_name=self.template_name, context = context)



class DetailPhotoView(DetailView):
    model = Photo
    template_name = 'photo_app/detail_photo.html'
    pk_url_kwarg = 'photo_id'
    context_object_name = 'photo'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(photo=self.object).order_by('-created_at')[:5]
        #Как сделать так, чтобы при наличии более 5 комментариев скрывались все, кроме 5 новых?
        #Остальные должны выводиться по кнопке "показать все". Асинхрон?
        return context



