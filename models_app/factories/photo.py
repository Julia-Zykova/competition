import os

import factory
from factory import fuzzy

from conf.settings.django import STATIC_ROOT
from models_app.factories.user import UserFactory
from models_app.models import Photo

path = STATIC_ROOT + "\images_for_tests\\"

list_images = os.listdir(path)

images = [path + image for image in list_images]


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    title = factory.Faker("sentence", nb_words=2)
    author = factory.SubFactory(UserFactory)

    image = factory.django.ImageField(from_path=fuzzy.FuzzyChoice(images))

    description = factory.Faker("sentence")
    pub_date = factory.Faker("date_time")
    state = factory.fuzzy.FuzzyChoice(choices=['in_moderation', 'approved', 'rejected', 'on_delete'])
    is_deleted = factory.Faker("boolean")
