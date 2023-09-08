import threading

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from .helpers import chat
from rasa.core.policies import ted_policy
# import threading
import json


class ChatBotConsumer(WebsocketConsumer):
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #
    #     # The consumer ChatConsumer is synchronous while the channel layer
    #     # methods are asynchronous. Therefore wrap the methods in async-to-sync
    #     async_to_sync(self.channel_layer.send)(
    #         self.channel_name,
    #         {
    #             "type": "chat_message",
    #             "text": {"msg": text_data_json["text"], "source": "user"},
    #         },
    #     )
    #
    #     # We will later replace this call with a celery task that will
    #     # use a Python library called ChatterBot to generate an automated
    #     # response to a user's input.
    #     async_to_sync(self.channel_layer.send)(
    #         self.channel_name,
    #         {
    #             "type": "chat.message",
    #             "text": {"msg": "Bot says hello", "source": "bot"},
    #         },
    #     )
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                "type": "chat_message",
                "text": {"msg": text_data_json["text"], "source": "user"},
            },
        )
        # get_response.delay(self.channel_name, text_data_json)
        thread = threading.Thread(target=chat, args=(self.channel_name, text_data_json,))
        thread.start()

    def chat_message(self, event):
        text = event["text"]
        self.send(text_data=json.dumps({"text": text}))