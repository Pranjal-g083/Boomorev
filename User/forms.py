from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    # password = forms.CharField(widget=forms.PasswordInput)
    # First_Name = forms.CharField(max_length=30)
    # Last_Name = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email' ]
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']