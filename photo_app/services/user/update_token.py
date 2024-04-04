from django import forms

from rest_framework.authtoken.models import Token

from models_app.models import CustomUser
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class UpdateTokenService(ServiceWithResult):
    user = ModelField(CustomUser)
    
    def process(self):
        if self.is_valid():
            self.result = self._regenerated_token
            return self

    
    def _token_delete(self):
        user = self.cleaned_data['user']
        user.auth_token.delete()
        
          
    @property
    def _regenerated_token(self):
        self._token_delete()
        return Token.objects.create(user = self.cleaned_data['user'])
        