"""WebSocket consumers for real-time chat."""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time chat in a conversation."""

    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'chat_message')
        if message_type == 'chat_message':
            await self.handle_chat_message(data)
        elif message_type == 'typing':
            await self.handle_typing(data)

    async def handle_chat_message(self, data):
        content = data.get('content', '')
        sender_type = data.get('sender_type', '')
        sender_id = data.get('sender_id', '')
        sender_name = data.get('sender_name', '')
        message = await self.save_message(content, sender_type, sender_id, sender_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': str(message.id),
                    'content': content,
                    'sender_type': sender_type,
                    'sender_id': sender_id,
                    'sender_name': sender_name,
                    'sent_at': message.sent_at.isoformat(),
                }
            }
        )

    async def handle_typing(self, data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'sender_name': data.get('sender_name', ''),
                'is_typing': data.get('is_typing', False),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'type': 'chat_message', 'message': event['message']}))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender_name': event['sender_name'],
            'is_typing': event['is_typing']
        }))

    @database_sync_to_async
    def save_message(self, content, sender_type, sender_id, sender_name):
        from .models import Message, Conversation
        conversation = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=conversation,
            content=content,
            sender_type=sender_type,
            sender_id=sender_id if sender_id else None,
            sender_name=sender_name
        )


class LawyerQueueConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for lawyer queue notifications."""

    async def connect(self):
        self.room_group_name = 'lawyers_queue'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def new_case(self, event):
        await self.send(text_data=json.dumps({'type': 'new_case', 'case': event['case']}))

    async def case_assigned(self, event):
        await self.send(text_data=json.dumps({
            'type': 'case_assigned',
            'case_id': event['case_id'],
            'lawyer_id': event['lawyer_id']
        }))