from django.urls import path

from photo_app.views.comment.delete import DeleteCommentView
from photo_app.views.photo.list import ListPhotoView
from photo_app.views.photo.upload import UploadPhotoView
from photo_app.views.photo.delete import DeletePhotoView
from photo_app.views.photo.detail import DetailPhotoView
from photo_app.views.photo.edit import EditPhotoView
from photo_app.views.personal_account.views import PersonalAccountView

app_name = 'photo_app'

urlpatterns = [
	path('', ListPhotoView.as_view(), name ='home'),
	path('upload/', UploadPhotoView.as_view(), name ='upload'),
	path('photo/<int:id>', DetailPhotoView.as_view(), name ='detail'),
	path('photo/<int:id>/delete/', DeletePhotoView.as_view(), name = 'delete'),
	path('photo/<int:id>/edit/', EditPhotoView.as_view(), name = 'edit'),
	path('user/<int:user_id>', PersonalAccountView.as_view(), name ='personal_account'),
	path('photo/<int:id>/comment_delete/', DeleteCommentView.as_view(), name = 'comment_delete'),
]
