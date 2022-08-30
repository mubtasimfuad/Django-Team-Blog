from django.contrib import admin
from django.template.defaultfilters import truncatechars

from .models import Post, Comment, Reply, Rereply

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    autocomplete_fields = ['author']
    # prepopulated_fields = {
    #     'slug': ['title']
    # }
    list_display = [ 'id', 'title', 'short_description', 'author', 'published_at', 'modified_at', "status"]
    list_editable = [ 'status']
    list_per_page = 10
    list_select_related = ['author']
    search_fields = ['title']
    list_filter = ['status', 'published_at', ]
    
    
    def short_description(self, post):
        return post.body if len(post.body) < 35 else (post.body[:33] + '..')

admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Rereply)


