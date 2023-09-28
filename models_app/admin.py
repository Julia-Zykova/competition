from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
	list_display = ('email', 'last_name', 'first_name')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'pub_date', 'slug')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'photo', 'text')

@admin.register(Voice)
class VoiceAdmin(admin.ModelAdmin):
	list_display = ('user', 'photo')
	
#admin.site.register(CustomUser)
#admin.site.register(Photo)
#admin.site.register(Comment)
#admin.site.register(Voice)