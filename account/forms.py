from dataclasses import field, fields
from django import forms
from . models import Account, AbstractBaseUser, Profile
from django.forms import inlineformset_factory

class RegistrationForm(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password again'}))
    is_admin = False
    is_active = False
    is_staff = False
    is_superadmin = False
    class Meta:
        model = Account
        fields = ['username' ,'email','first_name', 'last_name', 'gender','phone', 'password','employee_id']
        widgets = {
               'gender': forms.RadioSelect(attrs={'class': 'form-check form-check-inline', 'style': 'margin-right:2px'}),
               'password':forms.PasswordInput(attrs={'placeholder': 'provide a strong password '}),
               'employee_id': forms.TextInput(attrs={'placeholder': 'e.g: C17****'}),
               'phone':forms.TextInput(attrs={'placeholder': '+88018*******'})
           }   
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password doesn't match")

    def save(self):
        self.clean()
        user = self.Meta.model(
            username = self.cleaned_data['username'], 
            email = self.cleaned_data['email'], 
            first_name = self.cleaned_data['first_name'],
            last_name =  self.cleaned_data['last_name'],
            gender =  self.cleaned_data['gender'],
            phone =  self.cleaned_data['phone'],
            employee_id =  self.cleaned_data['employee_id'],


        )
        # Set password with method is solution
        user.set_password(self.cleaned_data['password']) 
        user.save()
        return user


''' inline formset_factory '''
ProfileUpdateFormset = inlineformset_factory(
    Account, Profile, 
    fields=('image', 'address','dob','linkedin', 'stake_overflow','github',))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =  '__all__'
        exclude = ('user',)
        widgets ={
             'image': forms.FileInput(attrs={'class': 'btn btn-dark  btn-sm'}),
             'dob': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            "dob": "Birth Date"}

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password again'}))
        new_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
        current_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Current'}))
        model=Account
        fields = ['username' ,'email','first_name', 'last_name','phone', 'password']
        



   