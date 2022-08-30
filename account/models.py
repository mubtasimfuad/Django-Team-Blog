from enum import unique
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django import forms
from django.urls import reverse

class MyAccountManger(BaseUserManager):
    def create_user(self, first_name,last_name, username,employee_id,email, password=None ):
        if not email:
            raise ValueError("User must have an email")
        
        if not username:
            raise ValueError("User must provide an username")
        if not employee_id:
            raise ValueError("User must provide an employee id")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            employee_id = employee_id,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user 

    def create_superuser(self,  first_name,last_name, username,employee_id, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            employee_id = employee_id,
            password=password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        user.save(using = self._db)

        return user

GENDER_CHOICES = [
('male', 'Male'),
('female', 'Female'),
('other', 'Other')
]



class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    employee_id = models.CharField(unique=True, max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(unique=True, max_length=100)
    phone = models.CharField(max_length=50)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=8,  default='male')


# Create your models here.
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['username' ,'email','first_name', 'last_name']

    objects = MyAccountManger()
    def __str__(self):
        return self.first_name + " "+ self.last_name+ " : "+self.employee_id

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    @property
    def get_profile(self):
         return self.user_profile.all()


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='user_profile')
    image = models.ImageField(upload_to='photos/profile', blank=True, default="profile.png")
    address = models.TextField(null=True)
    dob = models.DateField(null=True)
    linkedin = models.URLField(null=True)
    stake_overflow = models.URLField(null=True)
    github = models.URLField(null=True)
   
    
    def __str__(self) -> str:
        return str(self.user)

    # def get_absolute_url(self):
    #     return reverse("profile", kwargs={self.user.id})
    

