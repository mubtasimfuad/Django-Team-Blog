
from django.urls import reverse_lazy,reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.db.models import Count
from tags.models import Tag, TaggedItem
from .forms import CommentCreateForm, PostCreateOrUpdateForm, ReplyCreateForm, RereplyCreateForm
from .models import Post, Comment, Reply, Rereply

# Create your views here.


class PostListView(ListView):
    model = Post
    context_object_name = 'qs'
    queryset = Post.objects.filter(status="published")
    template_name = 'blog\list.html'
    tags = TaggedItem.objects.values('tag__label').annotate(total_count=Count('tag')).order_by('-total_count')[:10]
    extra_context = {"tags":tags}

    def get_queryset(self):
        return super().get_queryset().select_related('author')
    


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog\details.html'
    query_pk_and_slug =False
    
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            uuid = self.kwargs['uuid']
        ).select_related('author')
    

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['comments'] = Comment.objects.filter(post=context['post']).select_related('author').prefetch_related('comment_reply__author').prefetch_related('comment_reply__reply_rereplay__author')
        context['comment_form'] = CommentCreateForm()
        context['reply_form'] = ReplyCreateForm()
        context['rereply_form'] = RereplyCreateForm()

        return context


class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    template_name = 'blog\details.html'
    form_class = CommentCreateForm

    def get_success_url(self):
        return reverse('blog:blog_details', kwargs={'uuid': self.kwargs['uuid'],'slug':self.kwargs['slug'] })
    def form_valid(self, form):
        post = get_object_or_404(Post, uuid = self.kwargs ['uuid'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)


class ReplyCreateView(LoginRequiredMixin,CreateView):
    model = Reply
    template_name = 'blog\details.html'
    form_class = ReplyCreateForm

    def get_success_url(self):
        return reverse('blog:blog_details', kwargs={'uuid': self.kwargs['uuid'],'slug':self.kwargs['slug'] })
    def form_valid(self, form):
        comment = get_object_or_404(Comment, id = self.kwargs ['comment_id'])
        form.instance.author = self.request.user
        form.instance.comment = comment
        return super().form_valid(form)

class RereplyCreateView(LoginRequiredMixin,CreateView):
    model = Rereply
    template_name = 'blog\details.html'
    form_class = RereplyCreateForm

    def get_success_url(self):
        return reverse('blog:blog_details', kwargs={'uuid': self.kwargs['uuid'],'slug':self.kwargs['slug'] })
    def form_valid(self, form):
        reply = get_object_or_404(Reply, id = self.kwargs ['reply_id'])
        form.instance.author = self.request.user
        form.instance.reply = reply
        return super().form_valid(form)



    
   
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog\post_create_update.html'
    form_class = PostCreateOrUpdateForm
    extra_context = {'h1message': 'Create the post'}

    def form_valid(self, form) :
        form.instance.author = self.request.user
        return super().form_valid(form)
 


class PosUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog\post_create_update.html'
    form_class = PostCreateOrUpdateForm
    extra_context = {'h1message': 'Update the post'}
    pk_url_kwarg = 'post_id'

    def form_valid(self, form) :
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author





# class PostDeleteView(View):
#     model = Post
#     success_url = reverse_lazy('blog:blog_list')
#     template_name ='blog/delete.html'

#     def get_queryset(self,*args, **kwargs):
#         return super().get_queryset(*args, **kwargs).update(
#             status = 'deleted'
#         )


@login_required
def post_delete(request, post_id, *args, **kwargs):
    post = get_object_or_404(Post, id = post_id)
    if post.author != request.user:
        raise Http404
    else:
        post.status='deleted'
        post.save()
    return redirect("blog:blog_list")


# def post_update(request, post_id, *args, **kwargs):
#     post = Post.objects.get(id=post_id)
#     if request.method == 'POST':
#         form = PostCreateOrUpdateForm(request.POST, instance=post)
#         if form.is_valid():
#             post.save()
#             return redirect("blog:blog_details", post.slug, post.uuid)

#     else:
#         form = PostCreateOrUpdateForm(instance=post)
#     response = {
#         'form': form,
#         'h1message': 'Update the post',

#     }
#     return render(request, 'blog/post_create_update.html', response)


# def blog_details(request,slug,uuid, *args, **kwargs):
#     post = Post.objects.filter(uuid=uuid, slug=slug).first()
#     comments = Comment.objects.filter(post=post)


#     return render(request,'blog\details.html', {"post": post, "comments": comments})
