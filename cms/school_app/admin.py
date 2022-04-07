from django.contrib import admin
from .models import School, SchoolV2, SchoolV2Session, Post

# Register your models here.
admin.site.register(School)
admin.site.register(SchoolV2)
admin.site.register(SchoolV2Session)


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "created_on")
    list_filter = ("status",)
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
