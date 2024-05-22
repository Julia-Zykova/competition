from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from drf.views.photo.views import ListCreatePhotosAPIView, RetrieveUpdateDestroyPhotoAPIView

urlpatterns = [
    path('api/v1/', ListCreatePhotosAPIView.as_view()),
    path('api/v1/photo/<int:pk>/', RetrieveUpdateDestroyPhotoAPIView.as_view()),
    # path('api/v1/photo/<int:photo>/restore/'),

]
