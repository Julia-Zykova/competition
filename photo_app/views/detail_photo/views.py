from django.views.generic import DetailView
from django.shortcuts import render, redirect

from service_objects.services import ServiceOutcome

from models_app.models.photo.models import Photo
from models_app.models.comment.models import Comment

from photo_app.services.rename_photo import RenamePhotoService
from photo_app.services.delete_photo import SoftDeletePhotoService
from photo_app.services.restore_photo import RestorePhotoService
from photo_app.services.edit_description import EditDescriptionPhotoService

class DetailPhotoView(DetailView):
    #Просто View, без model
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

    def post(self, request,**kwargs):

        user = request.user

        try:
            photo = Photo.objects.get(pk=request.POST['photo'])
        except Exception as e:
            raise e
            
        if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
            if user._wrapped.__class__ == object:
                user._setup()
            user = user._wrapped

        #import pdb
        #pdb.set_trace()
        
        if request.POST['deleted'] == 'False':
            outcome = ServiceOutcome(
                SoftDeletePhotoService, request.POST.dict() |
                {'user': request.user, 'photo': photo})
            
        return redirect('home')

        #Передавать по нажатию информацию о действии "Изменить название/описание или удалить"
        #Если "Изменить", то редиректить на страницу, в которой будут поля для нового названия/описания
        #Если удалить, то удалять без редиректа
        #но с всплывающим сообщением "Фото можно восстановить в течение 1 дня с момента удаления"