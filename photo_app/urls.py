from django.urls import path
from photo_app.views.detail_photo.views import DetailPhotoView
from photo_app.views.list_photo.views import ListPhotoView
from photo_app.views.upload_photo.views import UploadPhotoView
from photo_app.views.personal_account.views import PersonalAccountView
from photo_app.views.personal_photo_list.views import PersonalPhotoListView

urlpatterns = [
	path('', ListPhotoView.as_view(), name='home'),
	path('upload/', UploadPhotoView.as_view(), name='upload'),
	path('photo/<int:photo_id>', DetailPhotoView.as_view(), name='detail'),
	path('user/<int:user_id>', PersonalAccountView.as_view(), name='personal_account'),
	path('user/<int:user_id>/photo/', PersonalPhotoListView.as_view(), name = 'personal_photo'),
]
