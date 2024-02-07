from django.contrib import admin
from .models import Profile


class UserProfile(admin.ModelAdmin):
    list_display = "bio", "avatar"


admin.site.register(Profile, UserProfile)
