from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
import uuid
import jwt
from social_netw.settings import SECRET_KEY
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# # Create your models here.
# class Car(models.Model):
# 	vin = models.CharField(db_index=True, unique= True, max_length=64)
# 	color = models.CharField(max_length=64)
# 	brand = models.CharField(max_length=64)
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)

class UserManager(BaseUserManager):
	def create_user(self, login, password=None):
		"""
		Create and save user with given data
		"""
		if not login:
			raise ValueError('User can not be created without login')
		user = self.model(login=login)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, login, password):
		if password is None:
			raise ValueError('Superuser must have a password')
		user = self.create_user(login, password=password)
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user

class User(AbstractBaseUser):
	login = models.CharField(max_length=32, unique=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	USERNAME_FIELD = 'login'
	REQUIRED_FIELDS = []
	objects = UserManager()

	def __str__(self):
		return self.login

	@property
	def token(self):
		return self.__generate_jwt_token()

	def __generate_jwt_token(self):
		dt = datetime.now() + timedelta(days=1)
		token = jwt.encode({'id': self.pk,'exp': int(dt.strftime('%s'))}, SECRET_KEY, algorithm='HS256')
		return token

class Post(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=64, blank=False)
	content = models.CharField(max_length=64, blank=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	like_count = models.IntegerField(default=0)
	dislike_count = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)