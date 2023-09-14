from django.urls import path
from .views import UploadPhotoView, ListPhotoView

urlpatterns = [
	path('', UploadPhotoView.as_view(), name='upload'),
	path('list', ListPhotoView.as_view(), name='home')
]
