# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests
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

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("I am from action file")
        dispatcher.utter_message(text="Hello World! action python code")

        return []

class ActionSearchRestaurant(Action):

    def name(self) -> Text:
        return "action_search_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message['entities']
        print(entities)

        for e in entities:
            if e['entity'] == 'hotel':
                name = e['value']
            if name == 'indian':
                message = "you selected Indian menu"
            if name == 'chinese':
                message = "you selected chinese menu"
            if name == 'italian':
                message = "you selected italian menu"
            if name == 'japanese':
                message = "you selected japanese menu"
        dispatcher.utter_message(text="search restaurants: "+message)

        return []

class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return "action_corona_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("https://data.covid19india.org/data.json").json()

        entities = tracker.latest_message['entities']
        print("Entities recorded from corona tracker: ",entities)
        state = None

        for e in entities:
            if e['entity'] == "state":
                state = e['value']
        
        message = "Please enter the correct name"
        for data in response["statewise"]:
            if data["state"] == state.title():
                print(data)
                message = "Active: "+data["active"] +" Confirmed: "+data["confirmed"] +" Recovered: "+data["recovered"]+" as on "+data['lastupdatedtime']
        
        dispatcher.utter_message(message)

        return []