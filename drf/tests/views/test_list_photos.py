from factory import fuzzy

from rest_framework.test import APITestCase

from drf.serializers import PhotoSerializer
from models_app.factories import UserFactory, PhotoFactory, VoiceFactory, CommentFactory
from models_app.models import Photo, CustomUser

from rest_framework.authtoken.models import Token

from django.db.models import Count, Q


class ListPhotosViewTest(APITestCase):

    def setUp(self):
        names = ["John", "Vi", "Jacky", "Joe", ]
        photo_titles = ["new photo", "title", "perfect image", "sunset", ]
        self.users = [UserFactory.create(first_name=name) for name in names]
        self.photos = [
            PhotoFactory.create(title=title, author=fuzzy.FuzzyChoice(self.users)) for title in photo_titles
        ]
        VoiceFactory.create_batch(15, user=fuzzy.FuzzyChoice(self.users))
        CommentFactory.create_batch(10, user=fuzzy.FuzzyChoice(self.users))

    def tearDowns(self):
        pass

    def test_without_params_status_200(self):
        response = self.client.get('/api/v1/photos/')
        self.assertEqual(response.status_code, 200)

    def test_with_sort_by_pubdate_params_status_200(self):
        params = {'orderby': 'pub_date'}
        response = self.client.get(
            '/api/v1/photos/',
            params
        )
        self.assertEqual(response.status_code, 200)

    def test_with_sort_by_sumvoices_params_status_200(self):
        params = {'orderby': '-voices'}
        response = self.client.get(
            '/api/v1/photos/',
            params
        )
        self.assertEqual(response.status_code, 200)
        photos = Photo.objects.exclude(state__in=['rejected', 'in_moderation']) \
            .annotate(sum=Count('voices')) \
            .order_by('-sum', '-pub_date')
        serializer = PhotoSerializer(photos, many=True)
        per_page = len(response.data['results'])
        self.assertEqual(response.data['results'], serializer.data[:per_page])

    def test_with_sort_by_sumcomments_params_status_200(self):
        params = {'orderby': '-comments'}
        response = self.client.get(
            '/api/v1/photos/',
            params
        )
        self.assertEqual(response.status_code, 200)
        photos = Photo.objects.exclude(state__in=['rejected', 'in_moderation']) \
            .annotate(sum=Count('comments')) \
            .order_by('-sum', '-pub_date')
        serializer = PhotoSerializer(photos, many=True)
        per_page = len(response.data['results'])
        self.assertEqual(response.data['results'], serializer.data[:per_page])

    def test_with_search_params_status_200(self):
        params = {'orderbysearch': 'new photo'}
        response = self.client.get(
            '/api/v1/photos/',
            params
        )
        self.assertEqual(response.status_code, 200)
        photos = Photo.objects.filter(
            Q(title__icontains='new photo') |
            Q(description__icontains='new photo') |
            Q(author__email__icontains='new photo')
        ).exclude(state__in=['rejected', 'in_moderation'])
        serializer = PhotoSerializer(photos, many=True)
        self.assertEqual(len(response.data['results']), len(serializer.data))

    def test_with_personal_list_params_status_200(self):
        params = {'personal_list': True}
        user = CustomUser.objects.get(first_name="Vi")
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            '/api/v1/photos/',
            params
        )
        self.assertEqual(response.status_code, 200)

    def test_with_personal_filter_params_status_200(self):
        params = {'personal_list': True, 'personal_filter': 'in_moderation'}
        user = CustomUser.objects.get(first_name="Vi")
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            '/api/v1/photos/',
            params,
        )
        self.assertEqual(response.status_code, 200)