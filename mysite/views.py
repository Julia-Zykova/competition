from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.urls import reverse_lazy
from service_objects.views import ServiceView

from .services.upload_photo import UploadPhotoService
from models_app.models.photo_model.forms import UploadPhotoForm
from models_app.models.photo_model.models import Photo
from models_app.models.user_model.models import CustomUser
from models_app.models.voice_model.models import Voice



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
                #post.author = request.CustomUser
                form.save()
            
            return redirect('upload')
            #else:
                #print(form.errors)
                #form = UploadPhotoForm()

                #return HttpResponse (f'что-то пошло не-так')
            #render(request, 'mysite/index.html', {'form': UploadPhotoForm})



class ListPhotoView(ListView):
    model = Photo
    template_name = 'mysite/list.html'
    paginate_by = 20

#Как обратиться к подсчету голосов в шаблоне? Кнопка тоже форма? Выносить как бизнес-логику, но как?
def vote(request, photo_id):
    photo =  get_object_or_404(Photo,pk = photo_id)
    to_vote = Vote.objects.create(photo = photo)
    to_vote.save()
    count_voices = Voice.objects.count(pk = photo_id)    

