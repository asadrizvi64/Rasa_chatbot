# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
import json
from rasa_sdk import Action, Tracker
from rasa.core.actions.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher


class ActionSubmitClaim(Action):
    def name(self) -> Text:
        return "action_submit_claim"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Implement logic to submit the claim (e.g., interact with your claims system)
        dispatcher.utter_message("Your claim has been submitted successfully.")
        return []


class ActionPolicyInformation(Action):
    def name(self) -> Text:
        return "action_provide_quote"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Implement logic to provide an insurance quote based on user input
        # policy_number = tracker.get_slot('policy_number')
        policy_number = tracker.latest_message['entities'][0]['value']
        end_point = "http://45.15.25.205:8007/chatbot/get_policy_info"
        data = {
            "policy_number": policy_number
        }
        response = requests.post(end_point, json=data)
        response = json.loads(response.text)
        if response.get('msg'):
            quote_message = response.get('msg')
        else:
            quote_message = response.get('policy_detail')



        # policy = PolicyInformation.objects.filter(policy_number=policy_number).first()


        # Example logic: Provide a quote based on the insurance type

        dispatcher.utter_message(quote_message)
        return []


# class ActionFallback(Action):
#     def name(self) -> Text:
#         return "action_fallback"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # Get the user's message that didn't match any intent
#         user_message = tracker.latest_message.get("text")
#
#         # Process the user's message (e.g., perform a specific action)
#         response_message = "I'm sorry, I didn't understand. Can you please rephrase your question?"
#
#         # Send the response back to the user
#         dispatcher.utter_message(text=response_message)
#
#         return []

class FallbackAction(Action):
    def name(self):
        return "action_fallback"

    def run(self, dispatcher, tracker, domain):
        # Define a response to off-topic input
        fallback_responses = [
            "I'm sorry, I couldn't understand that. Let's get back to ordering your pizza.",
            "That's an interesting topic, but let's focus on your pizza order. What type of pizza would you like?",
        ]

        # Select a random fallback response
        import random
        response = random.choice(fallback_responses)

        # Send the response to the user
        dispatcher.utter_message(response)

        return []


class PizzaOrderForm(FormAction):
    def name(self) -> Text:
        return "pizza_order_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["name", "pizza_type", "pizza_size", "toppings", "address", "phone_number"]

    def slot_mappings(self):
        return {
            "name": self.from_text(intent="provide_name"),
            "pizza_type": self.from_entity(entity="pizza_type"),
            "pizza_size": self.from_entity(entity="pizza_size"),
            "toppings": self.from_entity(entity="toppings"),
            "address": self.from_entity(entity="address"),
            "phone_number": self.from_entity(entity="phone_number"),
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        # Extract slot values and create the order here
        name = tracker.get_slot("name")
        pizza_type = tracker.get_slot("pizza_type")
        pizza_size = tracker.get_slot("pizza_size")
        toppings = tracker.get_slot("toppings")
        address = tracker.get_slot("address")
        phone_number = tracker.get_slot("phone_number")

        # You can add logic to place the order and provide a confirmation here
        dispatcher.utter_message(
            f"Thank you, {name}! Your {pizza_size} {pizza_type} pizza with {toppings} will be delivered to {address}. "
            f"We'll contact you at {phone_number} if needed. Enjoy your pizza!"
        )

        return []