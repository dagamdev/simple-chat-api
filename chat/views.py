from django.shortcuts import render
from rest_framework import viewsets
from .serializer import MessageSerializer
from .models import Message

# Create your views here.
class MessageView(viewsets.ModelViewSet):
  serializer_class = MessageSerializer
  queryset = Message.objects.all()