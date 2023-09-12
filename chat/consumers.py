import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class MessageType():
  id: str
  authorId: str
  content: str

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    print('🟢 Connection')
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = f'chat_{self.room_name}'
    print(self.room_name, self.room_group_name)

    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )
    await self.accept()

  async def disconnect(self, close_code):
    print(f'⚫ Disconnection closed with code: {close_code}')
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )

  async def receive(self, text_data):
    message: MessageType = json.loads(text_data)

    # print(message)

    # Send message to room group
    await self.channel_layer.group_send(
      self.room_group_name, 
      {
        'type': 'chat_message', 
        'message': message
      }
    )

  async def chat_message(self, event):
    message = event['message']

    # Send message to WebSocket
    await self.send(text_data=json.dumps(message))
