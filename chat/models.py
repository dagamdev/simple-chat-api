from django.db import models
from datetime import datetime
import uuid

# Create your models here.
class User(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4())
  name = models.CharField(max_length=150)
  # email = models.

class Message(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4())
  content = models.TextField()
  chat_id = models.UUIDField()
  author_id = models.UUIDField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.id)
