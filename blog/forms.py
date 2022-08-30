from django import forms

from blog.models import Comment, Post, Reply, Rereply


class PostCreateOrUpdateForm(forms.ModelForm):
    class Meta:
         model = Post
         fields ='__all__'
         exclude = ('author',)
    # class Media:
        # js = ('/site_media/static/tiny_mce/tinymce.min.js',)
    
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model =  Comment
        fields = '__all__'
        exclude = ('author','post',)
        labels = {
            'body': (''),
        }

class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model =  Reply
        fields = '__all__'
        exclude = ('author','comment',)
        labels = {
            'body': (''),
        }
class RereplyCreateForm(forms.ModelForm):
    class Meta:
        model =  Rereply
        fields = '__all__'
        exclude = ('author','reply',)

        labels = {
            'body': (''),
        }
    
    
    