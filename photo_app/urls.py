from django.urls import path
from .views import UploadPhotoView, ListPhotoView, DetailPhotoView

urlpatterns = [
	path('', ListPhotoView.as_view(), name='home'),
	path('upload', UploadPhotoView.as_view(), name='upload'),
	path('photo/<int:photo_id>', DetailPhotoView.as_view(), name='detail'),
]
