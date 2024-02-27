from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

from .views import *

urlpatterns = [
    path('signup/',UserSignup.as_view(), name = 'signup'),
    path('login/', UserLogin.as_view(), name = 'login'),
    path('userList/',UserList.as_view(), name = 'User List'),
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
    path('send-friend-request/', SendFriendRequestAPIView.as_view(), name='send-friend-request'),
    path('accept-friend-request/', AcceptFriendRequestAPIView.as_view(), name='accept-friend-request'),
    path('reject-friend-request/', RejectFriendRequestAPIView.as_view(), name='reject-friend-request'),
    path('list-friends/', FriendListAPIView.as_view(), name='list-friends'),
    path('pending-friend-requests/', PendingFriendRequestListAPIView.as_view(), name='pending-friend-requests'),
]