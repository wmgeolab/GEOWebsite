from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Post, School, SchoolV2, SchoolV2Session

# Register your models here.
admin.site.register(School)


class SchoolV2Admin(admin.ModelAdmin):
    # Reduce size of text inputs
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 1, "cols": 40})}
    }


admin.site.register(SchoolV2, SchoolV2Admin)


class SchoolV2SessionAdmin(admin.ModelAdmin):
    # Reduce size of text inputs
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 1, "cols": 40})}
    }


admin.site.register(SchoolV2Session, SchoolV2SessionAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "created_on")
    list_filter = ("status",)
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
