from django.urls import path, include
from post.views import *

app_name = 'post'

urlpatterns = [
    path('post/create/', PostCreateView.as_view()),
    path('all/', PostsListView.as_view()),
    path('post/detail/<int:pk>', PostDetailView.as_view()),
    path('users/', RegistrationApiView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    ]