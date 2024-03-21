from django import forms

from models_app.models import Comment
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class DeleteCommentService(ServiceWithResult):
    photo = forms.IntegerField()
    
    def process(self):
        if self.is_valid():
            self.result = self._delete
        return self
        
    @property
    def _comment(self):
       return Comment.objects.get(photo=self.cleaned_data['photo'])

    @property
    def _delete(self):
        self._comment.delete()