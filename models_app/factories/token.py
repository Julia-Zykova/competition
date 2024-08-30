import factory
from rest_framework.authtoken.models import Token

from models_app.factories.user import UserFactory


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token

    user = factory.SubFactory(UserFactory)
    key = factory.Faker("sha1")
