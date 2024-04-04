from django.urls import path

from photo_app.views.comment.views import CommentView
from photo_app.views.photo.views import ListPhotoView, UploadPhotoView, DeletePhotoView, DetailPhotoView, EditPhotoView
from photo_app.views.user.views import PersonalAccountView, UpdateTokenView
from photo_app.views.voice.views import VoiceView

app_name = 'photo_app'

urlpatterns = [
	path('', ListPhotoView.as_view(), name ='home'),
	path('vote/', VoiceView.as_view(), name = 'vote'),
	path('upload/', UploadPhotoView.as_view(), name ='upload'),
	path('photo/<int:id>/', DetailPhotoView.as_view(), name ='detail'),
	path('photo/<int:id>/delete/', DeletePhotoView.as_view(), name = 'delete'),
	path('photo/<int:id>/edit/', EditPhotoView.as_view(), name = 'edit'),
	path('user/<int:id>', PersonalAccountView.as_view(), name ='personal_account'),
	path('user/<int:id>/update_token/', UpdateTokenView.as_view(), name = 'update_token'),
	path('photo/<int:id>/comment/', CommentView.as_view(), name = 'comment'),
]
