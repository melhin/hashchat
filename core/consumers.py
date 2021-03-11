import json
from copy import deepcopy

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from core.apps import CoreConfig as tr


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'announcement',
                'sender':  self.scope["user"].email,
            }
        )
        await self.change_language(
                self.scope['user'], 'en')
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @sync_to_async
    def change_language(self, user, language_code):
        user.profile.language_code = language_code
        user.profile.save()

    @sync_to_async
    def get_language(self, user):
        return user.profile.language_code

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get('language'):
            await self.change_language(
                self.scope['user'], text_data_json['language'])

        else:
            message = text_data_json['message']
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message',
                    'sender':  self.scope["user"].email,
                    'message': message,
                    'language': await self.get_language(self.scope["user"]),
                }
            )

    # Receive message from room group
    async def message(self, event):
        message_event = deepcopy(event)
        lang = await self.get_language(self.scope["user"])
        if message_event['language'] != lang:
            message_event['message'] = tr.translator.translate(
                event['language'], lang, event['message'])[0]

        await self.send(text_data=json.dumps(message_event))

    # Receive message from room group
    async def announcement(self, event):

        await self.send(text_data=json.dumps(event))
