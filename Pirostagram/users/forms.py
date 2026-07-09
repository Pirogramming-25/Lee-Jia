from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'password1', 'password2')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'profile_image', 'introduction')