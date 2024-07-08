from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import RequestsClient

from drf.serializers import PhotoSerializer
from models_app.factories import UserFactory, PhotoFactory, VoiceFactory
from models_app.models import Photo

from django.db.models import Count, Q


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
        voices = VoiceFactory.create_batch(15)

    def tearDowns(self):
        pass

    def test_get_list_without_sorting(self):
        client = APIClient()
        response = client.get(reverse('photos'))
        photos = Photo.objects.exclude(state__in=['rejected', 'in_moderation'])
        serializer = PhotoSerializer(photos, many=True)
        per_page = len(response.data['results'])
        self.assertEqual(response.data['results'], serializer.data[:per_page])
        self.assertEqual(client.get(reverse('photos')).status_code, 200)

    def test_get_list_sort_by_pubdate(self):
        factory = APIRequestFactory()
        request = factory.get('photos/', {'orderby': '-pub_date'})
        client = APIClient()
        response = client.get(reverse('photos'))
        photos = Photo.objects.exclude(state__in=['rejected', 'in_moderation']) \
            .order_by('-pub_date')
        serializer = PhotoSerializer(photos, many=True)
        per_page = len(response.data['results'])
        self.assertEqual(response.data['results'], serializer.data[:per_page])
        self.assertEqual(client.get(reverse('photos')).status_code, 200)

    def test_get_list_sort_by_sumvoices(self):
        factory = APIRequestFactory()
        request = factory.get('photos/', {'orderby': '-voices'})
        client = APIClient()
        response = client.get(reverse('photos'))
        photos = Photo.objects.exclude(state__in=['rejected', 'in_moderation'])\
            .annotate(sum=Count('voices'))\
            .order_by('-sum', '-pub_date')
        serializer = PhotoSerializer(photos, many=True)
        per_page = len(response.data['results'])
        self.assertEqual(response.data['results'], serializer.data[:per_page])
        self.assertEqual(client.get(reverse('photos')).status_code, 200)

    def test_get_list_search(self):
        factory = APIRequestFactory()
        request = factory.get('photos/', {'orderbysearch': 'example'})
        client = APIClient()
        response = client.get(reverse('photos'))
        photos = Photo.objects.filter(
            Q(title__icontains='example') |
            Q(description__icontains='example') |
            Q(author__email__icontains='example')
        ).exclude(state__in=['rejected', 'in_moderation'])
        serializer = PhotoSerializer(photos, many=True)
        per_page = len(response.data['results'])
        self.assertEqual(response.data['results'], serializer.data[:per_page])
        self.assertEqual(client.get(reverse('photos')).status_code, 200)
