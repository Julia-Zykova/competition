import factory
from factory import fuzzy

from models_app.factories.user import UserFactory
from models_app.models import Photo


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    id = factory.Sequence(lambda n: n + 1)

    title = factory.Faker("sentence", nb_words=2)
    author = factory.SubFactory(UserFactory)

    image = factory.django.ImageField(from_path="media/photos/000/000/003/file/9I-bPcL0ICs.jpg")

    description = factory.Faker("sentence")
    pub_date = factory.Faker("date_time")
    state = factory.fuzzy.FuzzyChoice(choices=['in_moderation', 'approved', 'rejected', 'on_delete'])
    is_deleted = factory.Faker("boolean")
