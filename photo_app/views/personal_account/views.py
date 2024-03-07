from django.views.generic import DetailView
from django.shortcuts import render

from allauth.socialaccount.models import SocialAccount

from models_app.models.photo.models import Photo
from models_app.models.user.models import CustomUser
from models_app.models.voice.models import Voice
from models_app.models.comment.models import Comment
from photo_app.serializers import PhotoSerializer


class PersonalAccountView(DetailView):
    model = CustomUser
    template_name = 'photo_app/personal_account.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'user'
   
    
    


