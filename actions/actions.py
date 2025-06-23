
from rasa_sdk import Action
import requests

class ActionReferToProfessional(Action):
    def name(self):
        return "action_refer_to_professional"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        intent = tracker.latest_message['intent'].get('name')

        response = requests.post("http://your-node-backend.com/api/refer", json={
            "userId": user_id,
            "intent": intent
        })

        data = response.json()

        if data["success"]:
            dispatcher.utter_message(text=f"You are being referred to {data['professional']['full_name']} — {data['professional']['specialization']}.")
        else:
            dispatcher.utter_message(text="No professional is available right now, but we’ll notify you soon.")

        return []






# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
