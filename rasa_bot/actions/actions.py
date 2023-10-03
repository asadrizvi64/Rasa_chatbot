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

#
# class ActionSubmitClaim(Action):
#     def name(self) -> Text:
#         return "action_submit_claim"
#
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # Implement logic to submit the claim (e.g., interact with your claims system)
#         dispatcher.utter_message("Your claim has been submitted successfully.")
#         return []
#
#
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
#
#
# # class ActionFallback(Action):
# #     def name(self) -> Text:
# #         return "action_fallback"
# #
# #     def run(self, dispatcher: CollectingDispatcher,
# #             tracker: Tracker,
# #             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
# #         # Get the user's message that didn't match any intent
# #         user_message = tracker.latest_message.get("text")
# #
# #         # Process the user's message (e.g., perform a specific action)
# #         response_message = "I'm sorry, I didn't understand. Can you please rephrase your question?"
# #
# #         # Send the response back to the user
# #         dispatcher.utter_message(text=response_message)
# #
# #         return []
#
# class FallbackAction(Action):
#     def name(self):
#         return "action_fallback"
#
#     def run(self, dispatcher, tracker, domain):
#         # Define a response to off-topic input
#         fallback_responses = [
#             "I'm sorry, I couldn't understand that. Let's get back to ordering your pizza.",
#             "That's an interesting topic, but let's focus on your pizza order. What type of pizza would you like?",
#         ]
#
#         # Select a random fallback response
#         import random
#         response = random.choice(fallback_responses)
#
#         # Send the response to the user
#         dispatcher.utter_message(response)
#
#         return []
#
#
# class PizzaOrderForm(FormAction):
#     def name(self) -> Text:
#         return "pizza_order_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         return ["name", "pizza_type", "pizza_size", "toppings", "address", "phone_number"]
#
#     def slot_mappings(self):
#         return {
#             "name": self.from_text(intent="provide_name"),
#             "pizza_type": self.from_entity(entity="pizza_type"),
#             "pizza_size": self.from_entity(entity="pizza_size"),
#             "toppings": self.from_entity(entity="toppings"),
#             "address": self.from_entity(entity="address"),
#             "phone_number": self.from_entity(entity="phone_number"),
#         }
#
#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         # Extract slot values and create the order here
#         name = tracker.get_slot("name")
#         pizza_type = tracker.get_slot("pizza_type")
#         pizza_size = tracker.get_slot("pizza_size")
#         toppings = tracker.get_slot("toppings")
#         address = tracker.get_slot("address")
#         phone_number = tracker.get_slot("phone_number")
#
#         # You can add logic to place the order and provide a confirmation here
#         dispatcher.utter_message(
#             f"Thank you, {name}! Your {pizza_size} {pizza_type} pizza with {toppings} will be delivered to {address}. "
#             f"We'll contact you at {phone_number} if needed. Enjoy your pizza!"
#         )
#
#         return []

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import EventType
from rasa_sdk.forms import FormValidationAction
from typing import Text, List, Any, Dict
from rasa_sdk.events import SlotSet


# class ActionCalculateInsuranceQuote(Action):
#     def name(self):
#         return "action_calculate_insurance_quote"
#
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
#         # Access slots for relevant information
#         insurance_type = tracker.get_slot("insurance_type")
#         name = tracker.get_slot("name")
#
#         # Implement your logic to calculate the insurance quote here
#         # You can use the provided information like insurance_type and name
#         # Calculate the quote and provide a response
#         quote = 500  # Example quote
#
#         dispatcher.utter_message(f"Hi {name}, your {insurance_type} insurance quote is ${quote} per year.")
#         return []
#
#
# class ActionInterrupt(Action):
#     def name(self):
#         return "action_interrupt"
#
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
#         dispatcher.utter_message("Sure, how can I assist you now?")
#         return [SlotSet("requested_slot", None)]
#
#
# class ValidateInsuranceQuoteForm(Action):
#     def name(self):
#         return "validate_insurance_quote_form"
#
#     async def run(
#         self, dispatcher, tracker: Tracker, domain: DomainDict
#     ) -> dict:
#         # You can add custom validation logic here if needed
#         insurance_type = tracker.get_slot("insurance_type")
#
#         # Define a list of valid insurance types
#         valid_insurance_types = ["car", "home", "health"]
#
#         if insurance_type.lower() not in valid_insurance_types:
#             dispatcher.utter_message("I'm sorry, we currently only provide quotes for car, home, and health insurance.")
#             # Reset the slot to None since it's invalid
#             return [SlotSet("insurance_type", None)]
#
#         # Slot is valid, continue with the form
#         return [SlotSet("insurance_type", insurance_type)]

ALLOWED_PIZZA_SIZES = [
    "small",
    "medium",
    "large",
    "extra-large",
    "extra large",
    "s",
    "m",
    "l",
    "xl",
    "car",
    "home",
]
ALLOWED_PIZZA_TYPES = ["car", "home", "property", "pepperoni", "hawaii"]
VEGETARIAN_PIZZAS = ["mozzarella", "fungi", "veggie"]
MEAT_PIZZAS = ["pepperoni", "hawaii"]


class ValidateSimplePizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_pizza_form"

    def validate_insurance_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_PIZZA_SIZES:
            dispatcher.utter_message(text=f"We only accept pizza sizes: s/m/l/xl.")
            return {"pizza_size": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_size": slot_value}

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_type` value."""

        if slot_value not in ALLOWED_PIZZA_TYPES:
            dispatcher.utter_message(
                text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}."
            )
            return {"pizza_type": None}
        dispatcher.utter_message(text=f"OK! You want to {slot_value} pizza.")
        return {"pizza_type": slot_value}


class AskForVegetarianAction(Action):
    def name(self) -> Text:
        return "action_ask_vegetarian"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(
            text="Would you like to order a vegetarian pizza?",
            buttons=[
                {"title": "yes", "payload": "/affirm"},
                {"title": "no", "payload": "/deny"},
            ],
        )
        return []


class AskForPizzaTypeAction(Action):
    def name(self) -> Text:
        return "action_ask_pizza_type"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        if tracker.get_slot("vegetarian"):
            dispatcher.utter_message(
                text=f"What kind of pizza do you want?",
                buttons=[{"title": p, "payload": p} for p in VEGETARIAN_PIZZAS],
            )
        else:
            dispatcher.utter_message(
                text=f"What kind of pizza do you want?",
                buttons=[{"title": p, "payload": p} for p in MEAT_PIZZAS],
            )
        return []


class ValidateFancyPizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_fancy_pizza_form"

    def validate_vegetarian(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""
        if tracker.get_intent_of_latest_message() == "affirm":
            dispatcher.utter_message(
                text="I'll remember you prefer vegetarian."
            )
            return {"vegetarian": True}
        if tracker.get_intent_of_latest_message() == "deny":
            dispatcher.utter_message(
                text="I'll remember that you don't want a vegetarian pizza."
            )
            return {"vegetarian": False}
        dispatcher.utter_message(text="I didn't get that.")
        return {"vegetarian": None}

    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value not in ALLOWED_PIZZA_SIZES:
            dispatcher.utter_message(text=f"We only accept pizza sizes: s/m/l/xl.")
            return {"pizza_size": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_size": slot_value}

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_type` value."""

        if slot_value not in ALLOWED_PIZZA_TYPES:
            dispatcher.utter_message(
                text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}."
            )
            return {"pizza_type": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}."
            )
            return {"pizza_type": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_type": slot_value}


class ActionContractorInfo(Action):
    def name(self) -> Text:
        return "action_contractor_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Implement logic to provide an insurance quote based on user input
        # policy_number = tracker.get_slot('policy_number')
        contract_id = tracker.latest_message['entities'][0]['value']
        end_point = "http://45.15.25.205:8007/chatbot/get_contractor_info"
        data = {
            "contract_id": contract_id
        }
        response = requests.post(end_point, json=data)
        response = json.loads(response.text)
        if response.get('msg'):
            quote_message = response.get('msg')
        else:
            quote_message = response.get('description')

class ActionSubmitContractorInfo(Action):
    def name(self) -> Text:
        return "action_submit_contractor_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        # Implement logic to provide an insurance quote based on user input
        name = tracker.get_slot('name')
        description = tracker.get_slot('description')
        # contract_id = tracker.latest_message['entities'][0]['value']
        end_point = "http://45.15.25.205:8007/chatbot/get_contractor_info"
        data = {
            "name": name,
            "description": description
        }
        response = requests.post(end_point, json=data)
        response = json.loads(response.text)
        if response.get('msg'):
            quote_message = response.get('msg')
        else:
            quote_message = response.get('response')



# policy = PolicyInformation.objects.filter(policy_number=policy_number).first()


# Example logic: Provide a quote based on the insurance type

        dispatcher.utter_message(quote_message)
        return []