from rest_framework.test import APITestCase

from drf.serializers import UserSerializer
from models_app.factories import UserFactory, PhotoFactory
from models_app.models import Photo, CustomUser

from rest_framework.authtoken.models import Token

from conf.settings.django import STATIC_ROOT
from django.core.files.uploadedfile import SimpleUploadedFile


class CreatePhotosViewTest(APITestCase):

    def setUp(self):
        names = ["John", "Vi", "Jacky", "Joe", ]
        self.users = [UserFactory.create(first_name=name) for name in names]
        # self.img_path = STATIC_ROOT + "/images_for_tests/" + "/_wlOAQ-5tko.jpg/"

    def tearDowns(self):
        pass

    def test_create_with_all_params_status_201(self):
        user = CustomUser.objects.get(first_name="Vi")
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        img = SimpleUploadedFile(name="_wlOAQ-5tko.jpg", content_type="image/jpg", content=b"_wlOAQ-5tko")
        params = {
            'author': UserSerializer(user).data,
            'title': "Test title",
            'image': img,
            'description': "Test description",
        }

        response = self.client.post(
            '/api/v1/photos/',
            content_type="multipart/form-data",
            data=params,
        )
        self.assertEqual(response.status_code, 200)
