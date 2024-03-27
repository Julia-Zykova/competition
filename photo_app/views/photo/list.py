from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.renderers import JSONRenderer
from service_objects.services import ServiceOutcome

from models_app.models.photo.models import Photo
from models_app.models.user.models import CustomUser
from models_app.models.voice.models import Voice
from models_app.models.comment.models import Comment


from photo_app.services.voice.vote_for_photo import VoteForPhotoService
from photo_app.services.photo.get_list_of_photos import ListOfPhotoService
from photo_app.serializers import PhotoSerializer
from photo_app.utils import is_ajax

class ListPhotoView(View):
    context_object_name = 'posts'
    template_name = 'photo_app/list_of_photos.html'
    #permission_classes = (IsAuthenticatedOrReadOnly) 
   
    #Для авториз.польз. голосовал/нет с помощью annotate(?)

    def get(self, request,**kwargs):
        #import pdb
        #pdb.set_trace()

        outcome = ServiceOutcome(
            ListOfPhotoService, request.GET.dict() | {'user': request.user })

        if request.method == 'GET' and is_ajax(request):
            serialized_data = PhotoSerializer(outcome.result['page_obj'].object_list, many = True).data
            q_dict = {"posts": serialized_data, "page_number": outcome.result['page_number']}
            return JsonResponse(q_dict)

        elif request.method == 'GET'and not is_ajax(request):
            context = {"page_obj": outcome.result['page_obj'],
            "page_number": outcome.result['page_number'],
            "personal_list": outcome.result['personal_list']}
            return render(request, template_name=self.template_name, context = context)


    def post(self, request,**kwargs):
        
        user = request.user
            
        if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
            if user._wrapped.__class__ == object:
                user._setup()
            user = user._wrapped
        
        outcome = ServiceOutcome(
            VoteForPhotoService, request.POST.dict() |
            {'user': request.user })
        
        return redirect('photo_app:home')

