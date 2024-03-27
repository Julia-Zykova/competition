from django import forms

from models_app.models import Comment
from service_objects.services import ServiceWithResult

class EditCommentService(ServiceWithResult):

    comment = forms.IntegerField()
    text = forms.CharField(max_length=200)
    
    
    def process(self):
        if self.is_valid():
            self.result = self._update_comment
        return self

    @property
    def _comment(self):
       return Comment.objects.filter(id=self.cleaned_data['comment'])

    @property
    def _update_comment(self):
        self._comment.update(
            text = self.cleaned_data['text'],
            ) 
        return self