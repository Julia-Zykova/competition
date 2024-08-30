from django import forms
from rest_framework.authtoken.models import Token
from service_objects.services import ServiceWithResult

from models_app.models import CustomUser


class PersonalAccountService(ServiceWithResult):
    user = forms.IntegerField()

    def process(self):
        if self.is_valid():
            self._get_or_create_token
            self.result = self._user
            return self

    @property
    def _get_or_create_token(self):
        token, created = Token.objects.get_or_create(user=self._user)
        return {"token": token, "created": created}

    @property
    def _user(self):
        return CustomUser.objects.get(id=self.cleaned_data["user"])
