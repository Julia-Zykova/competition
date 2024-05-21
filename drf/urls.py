from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from drf.views.photo.views import ListCreatePhotosAPIView

urlpatterns = [
    path('api/v1/', ListCreatePhotosAPIView.as_view()),
    # path('api/v1/photo/<int:photo>/'),
    # path('api/v1/photo/<int:photo>/restore/'),

]
