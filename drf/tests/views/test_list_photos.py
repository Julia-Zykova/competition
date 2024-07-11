from django.urls import reverse

from rest_framework.test import APITestCase

from drf.serializers import PhotoSerializer
from models_app.factories import UserFactory, PhotoFactory, VoiceFactory, CommentFactory
from models_app.models import Photo, CustomUser

from rest_framework.authtoken.models import Token

from django.db.models import Count, Q


class ListPhotosViewTest(APITestCase):

    def setUp(self):
        PhotoFactory.create_batch(10)
        VoiceFactory.create_batch(15)
        CommentFactory.create_batch(10)

    def tearDowns(self):
        pass

    def test_get_list_without_sorting(self):
        response = self.client.get(reverse('photos'))
        photos = Photo.objects.exclude(state__in=['rejected', 'in_moderation'])
        serializer = PhotoSerializer(photos, many=True)
        per_page = len(response.data['results'])
        self.assertEqual(response.data['results'], serializer.data[:per_page])
        self.assertEqual(self.client.get(reverse('photos')).status_code, 200)

    def test_get_list_sort_by_pubdate(self):
        response = self.client.get(reverse('photos'), {'orderby': 'pub_date'})
        photos = Photo.objects.exclude(state__in=['rejected', 'in_moderation']) \
            .order_by('pub_date')
        serializer = PhotoSerializer(photos, many=True)
        per_page = len(response.data['results'])
        self.assertEqual(response.data['results'], serializer.data[:per_page])
        self.assertEqual(self.client.get(reverse('photos')).status_code, 200)

    def test_get_list_sort_by_sumvoices(self):
        response = self.client.get(reverse('photos'), {'orderby': '-voices'})
        photos = Photo.objects.exclude(state__in=['rejected', 'in_moderation']) \
            .annotate(sum=Count('voices')) \
            .order_by('-sum', '-pub_date')
        serializer = PhotoSerializer(photos, many=True)
        per_page = len(response.data['results'])
        self.assertEqual(response.data['results'], serializer.data[:per_page])
        self.assertEqual(self.client.get(reverse('photos')).status_code, 200)

    def test_get_list_sort_by_sumcomments(self):
        response = self.client.get(reverse('photos'), {'orderby': '-comments'})
        photos = Photo.objects.exclude(state__in=['rejected', 'in_moderation']) \
            .annotate(sum=Count('comments')) \
            .order_by('-sum', '-pub_date')
        serializer = PhotoSerializer(photos, many=True)
        per_page = len(response.data['results'])
        self.assertEqual(response.data['results'], serializer.data[:per_page])
        self.assertEqual(self.client.get(reverse('photos')).status_code, 200)

    def test_get_list_search(self):
        response = self.client.get(reverse('photos'), {'orderbysearch': 'example'})
        photos = Photo.objects.filter(
            Q(title__icontains='example') |
            Q(description__icontains='example') |
            Q(author__email__icontains='example')
        ).exclude(state__in=['rejected', 'in_moderation'])
        serializer = PhotoSerializer(photos, many=True)
        per_page = len(response.data['results'])
        self.assertEqual(response.data['results'], serializer.data[:per_page])
        self.assertEqual(self.client.get(reverse('photos')).status_code, 200)

    def test_get_list_personal_filter(self):
        user = CustomUser.objects.get(id=5)
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(reverse('photos'), {'personal_filter': True}, secure=True)
        photos = Photo.objects.filter(
                author=user,
                state__in=['in_moderation', 'approved', 'on_delete']
            )
        serializer = PhotoSerializer(photos, many=True)
        per_page = len(response.data['results'])
        self.assertEqual(response.data['results'], serializer.data[:per_page])

    # def test_get_list_max_params(self):
    #     response = self.client.get(reverse('photos'), {
    #         {'orderby': '-voices',
    #          }
    #     })
