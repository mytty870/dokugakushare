from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
#from django.contrib.auth import get_user_model User = get_user_model() 
from django.contrib.auth.password_validation import validate_password

class UserLoginForm(AuthenticationForm):
 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
 
    self.fields['username'].widget.attrs['class'] = 'form-control'
    self.fields['username'].widget.attrs['placeholder'] = 'メールアドレス'
  
    self.fields['password'].widget.attrs['class'] = 'form-control'
    self.fields['password'].widget.attrs['placeholder'] = 'パスワード'


class RegistForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)


    class Meta:
        model = User
        fields = ['username', 'email', "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ニックネーム'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード（確認）'


