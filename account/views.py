from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate,login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View
from account.forms import AccountUpdateForm, ProfileUpdateForm, RegistrationForm
from django.urls import reverse, reverse_lazy
from account.models import Account, Profile
from blog.models import Comment, Post, Reply, Rereply




class RegistrationView(UserPassesTestMixin,CreateView):
    model = Account
    template_name = 'accounts\\register.html'
    form_class = RegistrationForm
    success_url = "blog: blog_list"

    def test_func(self):
        return self.request.user.is_authenticated == False


def login(request):
    if request.user.is_authenticated == False:
        if request.method == 'POST':
            employee_id = request.POST['employee_id']
            password = request.POST['password']
            user_obj = Account.objects.filter(employee_id=employee_id).first()

            user = authenticate(employee_id=employee_id, password=password)

            if user is not None:
                auth_login(request,user)
                return redirect(reverse('account:profile', args=[user_obj.username]))
            else:
                messages.error(request,'Invalid login credential')
                return redirect(reverse('account:login'))
    else:
        raise Http404
    return render(request, 'accounts/login.html')
    


class LogoutView(UserPassesTestMixin,View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('account:login'))

    def test_func(self):
        return self.request.user.is_authenticated ==True

# class ProfileDetailsView(DetailView):
#     template_name = 'accounts\\profile.html'

class ProfileDetailsView(LoginRequiredMixin,UserPassesTestMixin, DetailView):
    model = Profile
    context_object_name ='profile'
    template_name = 'accounts\profile.html'
    slug_field = "user__username"
    slug_url_kwarg = "username"
    
    def get_queryset(self):
        return super().get_queryset().select_related('user')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_posts = Post.objects.filter(author=context['profile'].user).filter(~Q(status="deleted"))
        total_comment=0
        for post in user_posts:
            total_comment += post.total_comment
            
        post_count = user_posts.count()
        


        context["user_post"] = user_posts
        context["total_comment"] =  total_comment
        context["total_post"] =  post_count


        return context
    

    def test_func(self):
        
        return self.request.user.is_authenticated
        
# class ProfileUpdateView(UpdateView):
#     model = Profile
#     form_class = ProfileUpdateForm
#     template_name = 'accounts\profile_update.html'
#     slug_field = "user"
#     slug_url_kwarg = "user"
#     context_object_name = "profile_form"
    

class ProfileUpdateView(UpdateView):
    model = Account
    form_class = AccountUpdateForm
    template_name = 'accounts\profile_update.html'
    slug_field ="username"
    slug_url_kwarg ="username"
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs) 
        profile_obj = Profile.objects.get(user=self.request.user)

        if self.request.POST:
            context['profile'] = ProfileUpdateForm(self.request.POST,self.request.FILES, instance=profile_obj)
        else:
            context['profile'] = ProfileUpdateForm(instance=profile_obj)
        return context

    def form_valid(self, form) :

        context = self.get_context_data()
        profile = context['profile']
        self.object.save()
        if self.request.method=="POST":
            current_password = self.request.POST['current_password']
            if current_password == 

        if profile.is_valid():
            profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("account:profile", args=[self.object.username])

    
    
    








# class LoginView(View):
#     def post(self, request):
#         if request.method == 'POST':
#             employee_id = request.POST['employee_id']
#             password = request.POST['password']
#             user = authenticate(employee_id=employee_id, password=password)

#             if user is not None:
#                 auth_login(request,user)
#                 return HttpResponseRedirect(reverse('blog:blog_list'))
#             else:
#                 messages.error(request,'Invalid login credential')
#                 return HttpResponseRedirect('#')
#         return render(request, 'accounts/login.html')



    