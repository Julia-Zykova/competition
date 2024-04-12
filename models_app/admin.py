from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
	list_display = ('email', 'last_name', 'first_name', 'user_photo', 'id')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'pub_date', 'id')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'text')

@admin.register(Voice)
class VoiceAdmin(admin.ModelAdmin):
	list_display = ('user', 'photo')
	
