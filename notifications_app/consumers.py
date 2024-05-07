import json

from asgiref.sync import async_to_sync
from channels.exceptions import DenyConnection
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import AnonymousUser


class NotificationConsumer(WebsocketConsumer):
    def connect(self):

        if self.scope['user'] == AnonymousUser():
            raise DenyConnection('Пожалуйста авторизуйтесь')
        else:
            async_to_sync(self.channel_layer.group_add)(
                'user_' + str((self.scope['user']).id), self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'user_' + str((self.scope['user']).id), self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.send)(
            'user_' + str((self.scope['user']).id),
            {'type': 'user.message', 'message': message}

        )

    def user_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'event': 'send',
            'message': message
        }))
