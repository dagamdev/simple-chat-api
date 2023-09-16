import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class MessageType():
  id: str
  authorId: str
  content: str

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
    message: MessageType = json.loads(text_data)

    await self.channel_layer.group_send(
      self.conversation_group_name, 
      {
        'type': 'send_conversation_message', 
        'message': message
      }
    )

  async def send_conversation_message(self, event):
    message = event['message']

    # Send message to WebSocket
    await self.send(text_data=json.dumps(message))
