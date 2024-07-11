import factory

from models_app.factories.photo import PhotoFactory
from models_app.factories.user import UserFactory
from models_app.models import Comment


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    # comment = factory.SubFactory(CommentFactory)
    photo = factory.SubFactory(PhotoFactory)
    user = factory.SubFactory(UserFactory)
    text = factory.Faker("text")
