import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rasa.core.agent import Agent
import requests
# from rasa.core.interpreter import RasaNLUInterpreter
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.events import UserUttered, ActionExecuted
from rasa.shared.core.constants import ACTION_LISTEN_NAME
# rasa_agent = Agent.load("rasa_bot/models")
channel_layer = get_channel_layer()


def chat(channel_name, input_data):
    rasa_endpoint = "http://0.0.0.0:5005"

    message = {
        "message": input_data['text'],
    }

    # Send a POST request to the Rasa API
    response = requests.post(f"{rasa_endpoint}/webhooks/rest/webhook", json=message)

    if response.status_code == 200:
        rasa_response = response.json()
        messages = rasa_response[0]['text']
    else:
        # Handle the error, e.g., return an error response
        messages = "Failed to communicate with Rasa."
    async_to_sync(channel_layer.send)(
            channel_name,
            {
                "type": "chat.message",
                "text": {"msg": messages, "source": "bot"},
            },
        )
