from django.shortcuts import render
from rest_framework import generics, status
from post.serializers import *
from post.models import Post
from post.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from post.renderers import UserJSONRenderer
from rest_framework.generics import RetrieveUpdateAPIView


# Create your views here.
class PostCreateView(generics.CreateAPIView):
	serializer_class = OnePostSerializer

class PostsListView(generics.ListAPIView):
	serializer_class = PostListSerializer
	queryset = Post.objects.all()
	permission_classes = (IsAuthenticated, )

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = OnePostSerializer
	queryset = Post.objects.all()
	permission_classes = (IsOwnerOrReadOnly, )

class RegistrationApiView(APIView):
	permission_classes = (AllowAny, )
	# renderer_classes = (UserJSONRenderer,)
	serializer_class = RegistrationSerializer

	def post(self, request):
		user = request.data.get('user', {})
		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
	permission_classes = (AllowAny,)
	# renderer_classes = (UserJSONRenderer,)
	serializer_class = LoginSerializer

	def post(self, request):
		user = request.data.get('user', {})
		print(user)
		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
	permission_classes = (IsAuthenticated,)
	# renderer_classes = (UserJSONRenderer, )
	serializer_class = UserSerializer

	def retrieve(self, request, *args, **kwargs):
		serializer = self.serializer_class(request.user)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, *args, **kwargs):
		serializer_data = request.data.get('user', {})
		serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
