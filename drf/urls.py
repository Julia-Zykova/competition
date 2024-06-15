from django.urls import path

from drf.views.comment.views import ListCreateCommentsAPIView, RetrieveUpdateDestroyCommentAPIView
from drf.views.photo.views import ListCreatePhotosAPIView, RetrieveUpdateDestroyPhotoAPIView, UpdatePhotoRestoreAPIView
from drf.views.voice.views import CreateVoiceAPIView, DestroyVoiceAPIView

urlpatterns = [
    path('photos/', ListCreatePhotosAPIView.as_view()),
    path('photos/<int:photo>/', RetrieveUpdateDestroyPhotoAPIView.as_view()),
    path('photos/<int:photo>/restore/', UpdatePhotoRestoreAPIView.as_view()),
    path('photos/<int:photo>/comments/', ListCreateCommentsAPIView.as_view()),
    path('photos/<int:photo>/comments/<int:comment>/', RetrieveUpdateDestroyCommentAPIView.as_view()),
    path('photos/<int:photo>/vote/', CreateVoiceAPIView.as_view()),
    path('photos/<int:photo>/voice/<int:voice>/', DestroyVoiceAPIView.as_view()),
]


