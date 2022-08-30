from django.contrib import admin
from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
     path('', views.PostListView.as_view(), name="blog_list"),
     path('<uuid:uuid>'+'-'+'<slug:slug>/', views.PostDetailView.as_view(), name='blog_details'),
     path('post-create/', views.PostCreateView.as_view(), name="post_create"),
     path('post-update/<int:post_id>/', views.PosUpdateView.as_view(), name="post_update"),
     path('post-delete/<int:post_id>/', views.post_delete, name="post_delete"),
     path('add-comment/<uuid:uuid>'+'-'+'<slug:slug>/', views.CommentCreateView.as_view(), name="add_comment"),
     path('add-reply/<int:comment_id>/<uuid:uuid>'+'-'+'<slug:slug>/', views.ReplyCreateView.as_view(), name="add_reply"),
     path('add-rereply/<int:reply_id>/<uuid:uuid>'+'-'+'<slug:slug>/', views.RereplyCreateView.as_view(), name="add_rereply"),







  
]
