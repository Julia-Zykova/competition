from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import RequestsClient

from drf.serializers import PhotoSerializer
from models_app.factories import UserFactory, PhotoFactory
from models_app.models import Photo


# Using the standard RequestFactory API to create a form POST request
# factory = APIRequestFactory()
# request = factory.get('photos/', {})
#
# client = RequestsClient()
# response = client.get('http://testserver/users/')
# assert response.status_code == 200

class ListPhotosViewTest(APITestCase):

    def setUp(self):
        user = UserFactory.create_batch(3)
        photo = PhotoFactory.create_batch(10)

    def tearDowns(self):
        pass

    def test_get_list_without_sorting(self):
        client = APIClient()
        response = client.get(reverse('photos'))
        data = response.data['results']
        photos = Photo.objects.exclude(state__in=['rejected', 'in_moderation'])
        serializer = PhotoSerializer(photos, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(client.get(reverse('photos')).status_code, 200)

    def test_get_list_sort_by(self):
        factory = APIRequestFactory()
        request = factory.get('photos/', {'orderby': '-pub_date'})
        client = APIClient()
        response = client.get(reverse('photos'))
        data = response.data['results']
        photos = Photo.objects.exclude(state__in=['rejected', 'in_moderation']) \
            .order_by('-pub_date')
        serializer = PhotoSerializer(photos, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(client.get(reverse('photos')).status_code, 200)


