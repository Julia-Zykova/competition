from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.renderers import JSONRenderer


from models_app.models.photo.models import Photo
from models_app.models.user.models import CustomUser

from photo_app.serializers import PhotoSerializer
from photo_app.utils import is_ajax

class PersonalPhotoListView(ListView):
    model = Photo
    context_object_name = 'posts'
    template_name = 'photo_app/personal_photo_list.html'
        
    def get_queryset(self):
        user=self.request.GET.get('user')
        qs = Photo.objects.filter(author=user)
        return qs

    def get(self, request, *args, **kwargs):
        
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

        #if request.method == 'GET' and is_ajax(request):
        #    serialized_data = PhotoSerializer(page_obj.object_list, many = True).data
        #    q_dict = {"posts": serialized_data, "page_number": page_number}
        #    return JsonResponse(q_dict)

        if request.method == 'GET'and not is_ajax(request):
            context = {"page_obj": page_obj, "page_number": page_number}
            return render(request,template_name=self.template_name, context = context)


