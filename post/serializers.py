from rest_framework import serializers
from post.models import * 



class PostListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields  = ('id', 'title', 'content', 'user', 'like_count', 'dislike_count')

class OnePostSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	class Meta:
		model = Post
		fields  = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	token = serializers.CharField(max_length=255, read_only=True)

	class Meta:
		model = User
		fields = ['login', 'password', 'token']

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
	login = serializers.CharField(max_length=32, read_only=True)
	password = serializers.CharField(max_length=128, write_only=True)
	token = serializers.CharField(max_length=255, read_only=True)

	def validate(self, data):
		login = data.get('login', None)
		password = data.get('password', None)
		if login is None:
			raise serializers.ValidationError('An login is required to log in')
		if passwors is None:
			raise serializers.ValidationError('An passsword is required to log in')

		user = authenticate(username=login, password=password)
		if user is None:
			raise serializers.ValidationError('User with this email and password was not found')
		if not user.is_active:
			raise serializers.ValidationError('This user has been deactivated.')
		return {'login': user.username, 'token': user.token}
