from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from django import forms

from tasks.photo_reject import reject_photo


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'first_name', 'user_photo', 'id')
    fields = ['email', 'last_name', 'first_name', 'user_photo', 'id']
    readonly_fields = ['email', 'last_name', 'first_name', 'user_photo', 'id', 'personal_photo']

    @staticmethod
    def personal_photo(obj):
        return mark_safe(f'<img src="{obj.user_photo.url}">')


class VoiceInline(admin.TabularInline):
    model = Voice
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PhotoAdminForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = "__all__"

    def clean_state(self):
        if self.initial['state'] in ['approved', 'on_delete'] and self.cleaned_data['state'] == 'in_moderation':
            raise forms.ValidationError('Вы не можете направить фото на повторную модерацию')
        if self.initial['state'] == 'approved' and self.cleaned_data['state'] == 'rejected':
            raise forms.ValidationError('Вы не можете отклонить одобренное фото')
        elif self.initial['state'] == 'rejected' and self.cleaned_data['state'] == 'approved':
            raise forms.ValidationError('Вы не можете одобрить отклоненное фото')
        elif self.initial['state'] == 'on_delete' and self.cleaned_data['state'] in ['in_moderation', 'approved',
                                                                                     'rejected']:
            raise forms.ValidationError('Вы не можете сменить статус этого фото')
        elif self.initial['state'] == 'in_moderation' and self.cleaned_data['state'] == 'rejected':
            import environ
            env = environ.Env()

            result = reject_photo.apply_async(
                args=[self.instance.id],
                countdown=int(env('TIME_BEFORE_REJECT'))
            )
            return self.initial['state']

        return self.cleaned_data["state"]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    form = PhotoAdminForm
    list_display = ('title', 'author', 'pub_date', 'id', 'state')
    list_display_links = ('title', 'id')
    list_editable = ('state',)
    fields = ['state', 'author', 'title', 'pub_date', 'id', 'post_photo', 'image']
    readonly_fields = ['author', 'title', 'pub_date', 'id', 'post_photo', 'image']
    search_fields = ['author', 'title']
    list_filter = ['pub_date', 'state', 'title']

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # import pdb
        # pdb.set_trace()
        if 'state' in form.changed_data:
            if obj.state == "approved":
                channel_layer = get_channel_layer()
                author = obj.author
                message = f'Ваше фото "{obj.title}" было одобрено'
                obj.pub_date = datetime.datetime.now()
                async_to_sync(channel_layer.group_send)(
                    'user_' + str(author.id),
                    {
                        'type': 'user.message',
                        'message': message
                    }
                )

            super().save_model(request, obj, form, change)

    def save_form(self, request, form, change):
        if form.instance.state == 'rejected':
            import environ
            env = environ.Env()
            result = reject_photo.apply_async(
                args=[form.instance.id], countdown=int(env("TIME_BEFORE_REJECT"))
            )

            form.instance.state = 'in_moderation'
        return form.save(commit=False)



    def post_photo(self, obj):
        return mark_safe(f'<img src="{obj.photo_small.url}">')

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'state':
            kwargs['choices'] = (
                ('in_moderation', 'На модерации'),
                ('approved', 'Одобрено'),
                ('rejected', 'Отклонено'),
            )

        return super().formfield_for_choice_field(db_field, request, **kwargs)

    inlines = [
        VoiceInline,
        CommentInline
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'id')
    fields = ['user', 'text', 'photo', 'comments', 'id']
    readonly_fields = ['user', 'text', 'photo', 'comments', 'id']

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Voice)
class VoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'id')
    fields = ['user', 'photo', 'id']
    readonly_fields = ['user', 'photo', 'id']

    def has_delete_permission(self, request, obj=None):
        return False
