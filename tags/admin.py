from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from blog.models import Post

from tags.models import Tag, TaggedItem
from blog.admin import PostAdmin

# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['label']
class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


class CustomPostAdmin(PostAdmin):
    inlines = [TagInline]


admin.site.unregister(Post)
admin.site.register(Post, CustomPostAdmin)
