import factory

from models_app.models import CustomUser


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    id = factory.Sequence(lambda n: n + 1)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    password = factory.Faker("password")

    email = factory.LazyAttribute(lambda obj: f"{obj.first_name}.{obj.id}@example.com")

    is_staff = False
    is_superuser = False


class AdminFactory(UserFactory):
    is_staff = True
    is_superuser = True
