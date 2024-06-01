from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from drf.views.photo.views import ListCreatePhotosAPIView, RetrieveUpdateDestroyPhotoAPIView, UpdatePhotoRestoreAPIView

urlpatterns = [
    path('', ListCreatePhotosAPIView.as_view()),
    path('photo/<int:photo>/', RetrieveUpdateDestroyPhotoAPIView.as_view()),
    path('photo/<int:photo>/restore/', UpdatePhotoRestoreAPIView.as_view()),

]
