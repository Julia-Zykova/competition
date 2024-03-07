from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.renderers import JSONRenderer


from models_app.models.photo.models import Photo
from models_app.models.user.models import CustomUser
from models_app.models.voice.models import Voice
from models_app.models.comment.models import Comment
from photo_app.serializers import PhotoSerializer
from photo_app.utils import is_ajax

class ListPhotoView(ListView):
    model = Photo
    context_object_name = 'posts'
    template_name = 'photo_app/list_of_photos.html'

        
    def get_queryset(self):
        qs = Photo.objects.all()

        orderby = self.request.GET.get('orderby')

        if orderby:
            if orderby in ['voices', 'comments']: 
                qs = Photo.objects.all()\
                .annotate(sum=Count(orderby))\
                .order_by('sum')
            elif orderby in ['-voices', '-comments']:
                qs = Photo.objects.all()\
                .annotate(sum=Count(orderby[1:]))\
                .order_by('-sum')
            else:
               qs = Photo.objects.all().order_by(orderby)
        

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
        p = Paginator(qs, 8)
        page_number = request.GET.get('page')

        
        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)

        if request.method == 'GET' and is_ajax(request):
            print("Ajax")        

            serialized_data = PhotoSerializer(page_obj.object_list, many = True).data
            
            q_dict = {"posts": serialized_data, "page_number": page_number}              
            return JsonResponse(q_dict)

        elif request.method == 'GET'and not is_ajax(request):
            #import pdb
            #pdb.set_trace()
            context = {"page_obj": page_obj, "page_number": page_number}
            return render(request,template_name=self.template_name, context = context)

