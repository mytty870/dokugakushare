from django.urls import path
from . import views
from user.views import (
    IndexView, CategoryListView, SearchDetailView,
    CreatePostView, PostUpdateView, PostDeleteView, UserDetail,
    UserProfileUpdateView, PostDetailView, CommentFormView, SearchView
  
)



app_name ='user'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('search_detail/', SearchDetailView.as_view(), name='search_detail'),
    path('create/', CreatePostView.as_view(), name='create'),
    path('post_update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(),name='delete'),
    path('mypage/', UserDetail.as_view(), name='mypage'),
    path('user_profile_update/<int:pk>', UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('likes/', views.likes, name='likes'),
    path('comment/<int:pk>', CommentFormView.as_view(), name='comment'),
    path('search_view', SearchView.as_view(), name='search_view'),



]
