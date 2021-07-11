from django.urls import path
from .views import (
    RegistUserView, HomeView, UserLoginView,
    UserLogoutView,
)
from . import views



urlpatterns = [
    path('home/', HomeView.as_view(), name="home"),
    path('regist/', RegistUserView.as_view(), name="regist"),
    path('user_login/', UserLoginView.as_view(), name="user_login"),
    path('user_logout', UserLogoutView.as_view(), name="user_logout"),

    # path('user_create/', views.UserCreate.as_view(), name='user_create'),
    # path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    # path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),

]
