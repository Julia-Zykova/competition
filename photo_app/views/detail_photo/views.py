from django.views.generic import DetailView

from models_app.models.photo.models import Photo
from models_app.models.comment.models import Comment


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



