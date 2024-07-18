from rest_framework.test import APITestCase
from django.test.client import encode_multipart

from conf.settings.django import STATIC_ROOT
from models_app.factories import UserFactory

from rest_framework.authtoken.models import Token


class CreatePhotosViewTest(APITestCase):

    def setUp(self):
        self.user = UserFactory.create(first_name="Vi")
        self.token = Token.objects.get(user=self.user)
        self.img_path = STATIC_ROOT + "/images_for_tests/" + "/_wlOAQ-5tko.jpg"

    def tearDowns(self):
        pass

    def test_create_with_all_params_status_201(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        with open(
                self.img_path, "rb"
        ) as img:
            params = {
                'author': self.user,
                'title': "Test title",
                'image': img,
                'description': "Test description",
            }
            content = encode_multipart('BoUnDaRyStRiNg', params)
            content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'

            response = self.client.post(
                '/api/v1/photos/',
                content_type=content_type,
                data=content,
            )

        self.assertEqual(response.status_code, 201)
