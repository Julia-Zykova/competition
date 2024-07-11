import os

import factory
from factory import fuzzy

from models_app.factories.user import UserFactory
from models_app.models import Photo

images = os.path.join(
    "/mnt/c/Users/Юля/PycharmProjects/competition/media/photos/",
    os.listdir('/mnt/c/Users/Юля/PycharmProjects/competition/media/photos/')
)


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    title = factory.Faker("sentence", nb_words=2)
    author = factory.SubFactory(UserFactory)

    image = factory.django.ImageField(from_path=FuzzyChoice(images))

    description = factory.Faker("sentence")
    pub_date = factory.Faker("date_time")
    state = factory.fuzzy.FuzzyChoice(choices=['in_moderation', 'approved', 'rejected', 'on_delete'])
    is_deleted = factory.Faker("boolean")
