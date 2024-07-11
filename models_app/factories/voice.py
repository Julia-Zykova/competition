import factory

from models_app.factories.photo import PhotoFactory
from models_app.factories.user import UserFactory
from models_app.models import Voice


class VoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Voice

    photo = factory.SubFactory(PhotoFactory)
    user = factory.SubFactory(UserFactory)
    is_deleted = False


