from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from user.models import Post
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

class HomeView(ListView):
    template_name = 'home.html'
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-views')[:10]

class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        messages.success(self.request, 'ユーザー登録が完了しました。ログインしてみよう！')
        return super().form_valid(form)

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'user_login.html'
    authentication_form = UserLoginForm
    success_message = 'さんは、ログインに成功しました。さあ、投稿してみよう！'

class UserLogoutView(SuccessMessageMixin, LogoutView):
    success_message = 'ログアウトしました。'

