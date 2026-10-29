from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserCreationForm(UserCreationForm):
    class meta:
        model = User
        fields = ('username', 'email')

class UserChangeForm(UserChangeForm):
    class meta:
        model = User
        fields = ('username', 'email')