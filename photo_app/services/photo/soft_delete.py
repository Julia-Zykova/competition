from django import forms

from photo_app.tasks import delete_photo

from models_app.models import Photo
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class SoftDeletePhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    
    def process(self):
        if self.is_valid():
            self.result = self._soft_delete
        return self
        
    @property
    def _soft_delete(self):
        import environ
        env = environ.Env()
        result = delete_photo.apply_async(
            args=[self.cleaned_data['photo']], countdown=env('TIME_BEFORE_DELETE')
            )
        