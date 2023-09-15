import threading

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from .helpers import chat
from .models import Room, Message
from rasa.core.policies import ted_policy
# import threading
import json


class ChatBotConsumer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None  # new
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        if self.room_name == 'newChat':
            room = Room.objects.create(name=self.scope['user'])
            name = f'{room.name}_{room.id}'
            room.name = name
            room.save()
            self.room_name = room.name
        else:
            self.room_name = Room.objects.filter(name=self.room_name).first()
        self.room_group_name = f'{self.room_name.name}'
        # self.room = Room.objects.get(name=self.room_name)
        self.user = self.scope['user']  # new

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        room = Room.objects.filter(name=self.room_name).first()
        messages = Message.objects.filter(user=self.user, room=room).order_by('id')
        self.send(json.dumps(
        {
                "type": "conservation",
                "messages": [message.content for message in messages]
            },
        ))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if not self.user.is_authenticated:  # new
            return

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "text": {"msg": text_data_json["text"], "source": "user"},
            },
        )
        # get_response.delay(self.channel_name, text_data_json)
        thread = threading.Thread(target=chat, args=(self.room_group_name, text_data_json, self.user))
        thread.start()

    def chat_message(self, event):
        text = event["text"]
        self.send(text_data=json.dumps({"text": text}))