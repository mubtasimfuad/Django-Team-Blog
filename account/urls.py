from django.contrib import admin
from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/<slug:username>/', views.ProfileDetailsView.as_view(), name='profile'),
    path('profile-update/<slug:username>/', views.ProfileUpdateView.as_view(), name='profile_update'),

]
