from django.shortcuts import redirect
from django.views.generic import View
from service_objects.services import ServiceOutcome

from photo_app.services.voice.vote_for_photo import VoteForPhotoService


class VoiceView(View):
    # permission_classes = (IsAuthenticatedOrReadOnly)

    def post(self, request):
        ServiceOutcome(
            VoteForPhotoService,
            request.POST.dict() | {"user": request.user if self.request.user.is_authenticated else None},
        )

        return redirect("photo_app:home")
