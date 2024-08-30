from channels.layers import get_channel_layer
from django.shortcuts import redirect, render
from django.views.generic import View
from service_objects.services import ServiceOutcome

from models_app.models.photo.models import Photo
from photo_app.services.user.personal_account import PersonalAccountService
from photo_app.services.user.update_token import UpdateTokenService


class PersonalAccountView(View):
    # permission_classes = (IsAuthenticated)

    def get(self, request, **kwargs):

        outcome = ServiceOutcome(
            PersonalAccountService,
            request.GET.dict()
            | {
                "user": self.kwargs["id"],
            },
        )
        get_channel_layer()
        return render(
            request,
            template_name="photo_app/personal_account.html",
            context={"user": outcome.result, "photo": Photo.objects.filter(author=outcome.result.id)[:4]},
        )


class UpdateTokenView(View):
    # permission_classes = (IsAuthenticated)

    def post(self, request, **kwargs):

        ServiceOutcome(
            UpdateTokenService,
            request.POST.dict()
            | {
                "user": request.user if self.request.user.is_authenticated else None,
            },
        )
        return redirect("photo_app:personal_account", id=self.kwargs["id"])
