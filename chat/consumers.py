import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from . import models

class ConversationConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    # print('🟢 Socket connection')
    self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
    self.conversation_group_name = f'conversation_{self.conversation_id}'

    await self.channel_layer.group_add(
      self.conversation_group_name,
      self.channel_name
    )
    await self.accept()

  async def disconnect(self, close_code):
    # print(f'Disconnection closed with code: {close_code}')
    await self.channel_layer.group_discard(
      self.conversation_group_name,
      self.channel_name
    )

  async def receive(self, text_data):
    pre_message = json.loads(text_data)

    new_message = await self.save_data_message(pre_message)
    # print(new_message)

    message = {
      'id': str(new_message.id),
      'read': new_message.read,
      'author': str(new_message.author.id),
      'content': new_message.content,
      'created_at': str(new_message.created_at).replace(' ', 'T'),
      'updated_at': str(new_message.updated_at).replace(' ', 'T'),
      'conversation': str(new_message.conversation.id)
    }
    
    # print(message)

    await self.channel_layer.group_send(
      self.conversation_group_name, 
      {
        'type': 'send_conversation_message', 
        'message': message
      }
    )

  async def send_conversation_message(self, event):
    message = event['message']

    await self.send(text_data=json.dumps(message))

  @database_sync_to_async
  def create_data_message(self, author: str, content: str, conversation: str):
    author_inst = models.CustomUser.objects.get(id=author)
    conversation_inst = models.Conversation.objects.get(id=conversation)

    return models.Message.objects.create(author=author_inst, content=content, conversation=conversation_inst)

  async def save_data_message(self, preMessage):
    return await self.create_data_message(preMessage['author'], preMessage['content'], preMessage['conversation'])

