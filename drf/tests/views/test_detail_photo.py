from rest_framework.test import APITestCase

from models_app.factories import UserFactory, PhotoFactory
from models_app.models import Photo, CustomUser

from rest_framework.authtoken.models import Token


class DetailPhotoViewTest(APITestCase):

    def setUp(self):
        self.user = UserFactory.create(first_name="Vi")
        self.token = Token.objects.get(user=self.user)
        self.photo_approved = PhotoFactory(state="approved", is_deleted=False, author=self.user)
        self.photo_in_moderation = PhotoFactory(state="in_moderation", is_deleted=False, author=self.user)

    def tearDowns(self):
        pass

    def test_detail_photo_status_200(self):
        response = self.client.get(f'/api/v1/photos/{self.photo_approved.id}/')
        self.assertEqual(response.status_code, 200)

    def test_detail_photo_in_moderation_404(self):
        response = self.client.get(f'/api/v1/photos/{self.photo_in_moderation.id}/')
        self.assertEqual(response.status_code, 404)

    def test_detail_photo_in_moderation_for_author_status_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(f'/api/v1/photos/{self.photo_in_moderation.id}/')
        self.assertEqual(response.status_code, 200)