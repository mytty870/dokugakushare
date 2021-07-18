from django.urls import path
from . import views
from user.views import (
    SearchDetailView,
    CreatePostView, PostUpdateView, PostDeleteView, UserDetail,
    UserProfileUpdateView, PostDetailView, CommentFormView, SearchView,
    CommentReplyFormView, IndividualPageView
  
)



app_name ='user'

urlpatterns = [
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('search_detail/', SearchDetailView.as_view(), name='search_detail'),
    path('create/', CreatePostView.as_view(), name='create'),
    path('post_update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(),name='delete'),
    path('mypage/', UserDetail.as_view(), name='mypage'),
    path('user_profile_update/<int:pk>', UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('likes/', views.likes, name='likes'),
    path('comment/<int:pk>', CommentFormView.as_view(), name='comment'),
    path('search_view', SearchView.as_view(), name='search_view'),
    path('comment_reply/<int:pk>', CommentReplyFormView.as_view(), name='comment_reply'),
    path('individualpage/<int:pk>', IndividualPageView.as_view(), name='individualpage'),



]

