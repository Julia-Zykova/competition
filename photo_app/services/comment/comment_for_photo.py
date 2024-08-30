from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django import forms
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import Comment, CustomUser, Photo


class CommentForPhotoService(ServiceWithResult):
    photo = forms.IntegerField(required=False)
    user = ModelField(CustomUser)
    text = forms.CharField(
        max_length=200,
        required=True,
        error_messages={
            "max_length": "Слишком длинный комментарий.",
            "required": "Вы не можете оставить пустой комментарий",
        },
    )
    comment = forms.IntegerField(required=False)

    def process(self):
        if self.is_valid():
            self.result = self._comment
        return self

    @property
    def _photo(self):
        photo = Photo.objects.get(id=self.cleaned_data["photo"])
        if photo.state == "approved":
            return photo
        else:
            raise forms.ValidationError("Вы не можете оставить комментарий к этому фото")

    @property
    def _parent_comment(self):
        return Comment.objects.get(id=self.cleaned_data["comment"])

    @property
    def _comment(self):
        channel_layer = get_channel_layer()
        author = self._photo.author

        if self.cleaned_data["comment"]:
            return Comment.objects.create(
                user=self.cleaned_data["user"],
                text=self.cleaned_data["text"],
                comment=self._parent_comment,
            )
        else:
            obj = Comment.objects.create(
                user=self.cleaned_data["user"],
                text=self.cleaned_data["text"],
                photo=self._photo,
            )
            sum_сomments = self._photo.comments.count()
            message = (
                f'Пользователь {self.cleaned_data["user"]} оставил комментарий к вашему фото "{self._photo.title}".'
                f"Всего комментариев: {sum_сomments}."
            )
            async_to_sync(channel_layer.group_send)(
                "user_" + str(author.id), {"type": "user.message", "message": message}
            )
            return obj
