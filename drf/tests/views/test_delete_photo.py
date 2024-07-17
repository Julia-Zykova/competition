from rest_framework.test import APITestCase

from models_app.factories import UserFactory, PhotoFactory
from models_app.models import Photo, CustomUser

from rest_framework.authtoken.models import Token


class DeletePhotoViewTest(APITestCase):

    def setUp(self):
        self.user = UserFactory.create(first_name="Vi")
        self.photo = PhotoFactory(state="approved", is_deleted=False, author=self.user)

    def tearDowns(self):
        pass

    def test_delete_photo_status_204(self):
        user = CustomUser.objects.get(first_name="Vi")
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(f'/api/v1/photos/{self.photo.id}/')
        self.assertEqual(response.status_code, 204)
