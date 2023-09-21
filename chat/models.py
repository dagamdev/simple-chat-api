from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
class UserManager(BaseUserManager):
  def create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError('El Email es obligatorio')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if not extra_fields.get('is_staff'):
      raise ValueError('Superuser debe tener is_staff=True.')
    if not extra_fields.get('is_superuser'):
      raise ValueError('Superuser debe tener is_superuser=True.')

    return self.create_user(email, password, **extra_fields)
  
def validate_username(value):
  if any(char.isdigit() for char in value):
    raise ValidationError("El nombre de usuario no puede contener números.")

class CustomUser(AbstractBaseUser):
  id = models.UUIDField(primary_key=True, default=uuid4)
  email = models.EmailField(max_length=254, unique=True)
  password = models.CharField(max_length=128, null=True)
  username = models.CharField(unique=True, max_length=30, validators=[
    RegexValidator(
      regex=r'^[a-zA-Z0-9_-]+$',
      message="El nombre de usuario no puede contener otro tipo de caracteres que no sean guiones o guiones bajos.",
      code='invalid_username'
    ),
    validate_username,
  ])
  avatar_url = models.URLField(null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email
  
  def has_module_perms(self, app_label):
    return True
  
  def has_perm(self, perm, obj=None):
    return True


class Conversation(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid4)
  participants = models.ManyToManyField(CustomUser, related_name='conversations')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f'Conversation: {str(self.id)}'

class Message(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid4)
  read = models.BooleanField(default=False)
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  content = models.TextField(max_length=2000)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.author} {str(self.id)}'