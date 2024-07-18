import json

from rest_framework.test import APITestCase

from models_app.factories import UserFactory, PhotoFactory
from models_app.models import CustomUser

from rest_framework.authtoken.models import Token


class UpdatePhotoViewTest(APITestCase):

    def setUp(self):
        self.user = UserFactory.create(first_name="Vi")
        self.token = Token.objects.get(user=self.user)
        self.photo = PhotoFactory(
            title="test_title", description="test_description", state="approved", is_deleted=False, author=self.user
        )

    def tearDowns(self):
        pass

    def test_update_photo_with_title_params_status_200(self):
        params = {'title': 'Updated_title'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(f'/api/v1/photos/{self.photo.id}/', params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated_title')

    def test_update_photo_with_description_params_status_200(self):
        params = {'description': 'Updated_description'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(f'/api/v1/photos/{self.photo.id}/', params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], 'Updated_description')

    def test_update_photo_with_title_and_desc_params_status_200(self):
        params = {'title': 'Updated_title', 'description': 'Updated_description'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(f'/api/v1/photos/{self.photo.id}/', params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated_title')
        self.assertEqual(response.data['description'], 'Updated_description')