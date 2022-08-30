
from pickle import TRUE
from tabnanny import verbose
from django.db import models
from account.models import Account
from django.urls import reverse
from django.template.defaultfilters import slugify
from uuid import uuid4
from tinymce.models import HTMLField



#  models here.
class Post(models.Model):
    STATUS_PUBLISH = 'published'
    STATUS_DRAFT = 'draft'
    STATUS_DELETED = 'deleted'

    STATUS_CHOICES = [
        (STATUS_PUBLISH, 'Published'),
        (STATUS_DRAFT, 'Draft'),
        (STATUS_DELETED, 'Deleted')
    ]

    uuid = models.UUIDField(default=uuid4, editable=False, null= True)
    title = models.CharField(max_length=351)
    body = HTMLField()
    author = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    published_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True , editable=False)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    slug = models.SlugField(null=True, editable=False, blank=True)

    def __str__(self) -> str:
        return self.title 

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    class Meta:
        ordering = ['-published_at']
        unique_together = ['uuid','title']

    def get_absolute_url(self):
        return reverse("blog:blog_details", args=[  self.uuid, self.slug])

    @property
    def total_comment(self):
        comments = Comment.objects.filter(post=self.id).prefetch_related('comment_reply')
        comments_count = comments.count()
        reply=Reply.objects.filter(comment__in= comments).prefetch_related('reply_rereplay')
        reply_count = reply.count()
        rereply = Rereply.objects.filter(reply__in=reply)
        rereply_count =rereply.count()
        total_comment = comments_count+reply_count+rereply_count

        return total_comment

        
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment' )
    body = models.TextField()
    author = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='blog_comments')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    published_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True , editable=False)

    @property
    def get_replies(self):
        return self.comment_reply.all()
    @property
    def get_profile(self):
        return self.author.user_profile
    
    

    class Meta:
        ordering =['-created_at']

    def __str__(self) -> str:
        return  self.post.title[:30]+" "+self.body[:30] 
   

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='comment_reply')
    body = models.TextField()
    author = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='blog_replies')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    published_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True , editable=False)
    
    @property
    def get_rereplies(self):
        return self.reply_rereplay.all()
    @property
    def get_profile(self):
        return self.author.user_profile

    def __str__(self) -> str:
        return  self.body[:30] + " "+self.author.first_name 

    class Meta:
        verbose_name_plural = "Replies"

class Rereply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE,related_name='reply_rereplay')
    body = models.TextField()
    author = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='blog_rereplies')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    published_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True , editable=False)
    
   
    def __str__(self) -> str:
        return  self.reply.body[:30] + " "+self.author.first_name 

    class Meta:
        verbose_name_plural = "Re Replies"
    @property
    def get_profile(self):
        return self.author.user_profile

    # class Vote(models.Model):
    #     voted_by =  models.ForeignKey(
    #     Account, on_delete=models.CASCADE, related_name='blog_votes')
        

#flake8