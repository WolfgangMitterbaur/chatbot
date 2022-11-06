"""
Created on 29.10.2022
@author: Wolfgang Mitterbaur

classes for rasa actions of the hotel booking chatbot
"""

from . import mycsvfileoperation
import random
from typing import Text, List, Any, Dict, Optional, Union
from rasa_sdk import Action, Tracker, FormValidationAction 
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

class ValidateNameForm(FormValidationAction):
    """
    Validate the input of the names form
    """  
    def name(self) -> Text:
        return "validate_name_form"

    def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""

        # check user input
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"That's a very short name. I'm assuming you mis-spelled.")
            return {"first_name": None}
        else:
            return {"first_name": slot_value}

    def validate_last_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `last_name` value."""

        # check user input
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"That's a very short name. I'm assuming you mis-spelled.")
            return {"last_name": None}
        else:
            
            return {"last_name": slot_value}
        
    def validate_email_address(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `email_address` value."""
        
        # check user input: length of email, the @ is mandatory
        if len(slot_value) <= 5:
            dispatcher.utter_message(text=f"That's a very short email. I'm assuming you mis-spelled.")
            return {"email_address": None}
        elif not "@" in slot_value:
            dispatcher.utter_message(text=f"That's a very unusual email. I'm assuming you mis-spelled.")
            return {"email_address": None}
        else:
            
            # identify regular guest from database
            slot_first_name = tracker.get_slot('first_name')
            slot_last_name = tracker.get_slot('last_name')
            slot_checkin_date = tracker.get_slot('checkin_date')
            slot_checkout_date = tracker.get_slot('checkout_date')
            slot_number_guests = tracker.get_slot('number_guests')
            slot_number_rooms = tracker.get_slot('number_rooms')
            slot_room_type = tracker.get_slot('room_type')
            
            file_operator = mycsvfileoperation.GuestDatabase("clientdatabase.csv")
            all_clients = file_operator.read_data()
            
            for i in range(0, len(all_clients)):
                
                a_client = all_clients[i]
            
                if (a_client.first_name == slot_first_name and a_client.last_name == slot_last_name and a_client.email_address == slot_value) :
                    dispatcher.utter_message(text=f"Nice to welcome you again.")
                    
                    return {"phone": a_client.phone_number, "email_address": slot_value}
            
            return {"email_address": slot_value}
        
    def validate_phone(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `phone` value."""
        
        # check user input: length of phone number
        if len(slot_value) < 8:
            dispatcher.utter_message(text=f"That's a very short phone number. I'm assuming you mis-spelled.")
            return {"phone": None}
        else:
            
            return {"phone": slot_value}
 
class ValidateRooomForm(FormValidationAction):
    """
    Validate the input of the rooms form
    """
    def name(self) -> Text:
        return "validate_room_form"

    def validate_checkin_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `checkin_date` value."""
        
        # check user input: length of date
        if len(slot_value) <= 5:
            dispatcher.utter_message(text=f"That's a  short check-in date. I'm assuming you mis-spelled.")
            return {"checkin_date": None}
        else:
            return {"checkin_date": slot_value}

    def validate_checkout_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `checkout_date` value."""
        
        # check user input: length of date        
        if len(slot_value) <= 5:
            dispatcher.utter_message(text=f"That's a  short check-out date. I'm assuming you mis-spelled.")
            return {"checkout_date": None}
        else:
            return {"checkout_date": slot_value}
     
    def validate_number_guests(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `number_guests` value."""
        
        # check user input
        if len(slot_value) < 1:
            dispatcher.utter_message(text=f"That's a  short number of guests. I'm assuming you mis-spelled.")
            return {"number_guests": None}
        else:
            return {"number_guests": slot_value}

    def validate_number_rooms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `number_rooms` value."""
        
        # check user input
        if (slot_value != "1" and slot_value != "2"):            
            dispatcher.utter_message(text=f"I am sorry, you can book only 1 or 2 rooms with the bot.")
            return {"number_rooms": None}
        else:
            return {"number_rooms": slot_value}

    def validate_room_type(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `room_type` value."""
        
        # check user input: only one, two and double are allowed
        if ("one" in slot_value or "two" in slot_value or "double" in slot_value):
                                  
            return {"room_type": slot_value}
        
        else:
             
            dispatcher.utter_message(text=f"We offer only one, two or double bed rooms.")
            return {"room_type": None}

class ActionStoreClientRoom(Action):
    """
    Store client reservation
    """
    def name(self) -> Text:
        return "action_store_client_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        slot_first_name = tracker.get_slot('first_name')
        slot_last_name = tracker.get_slot('last_name')
        slot_email_address = tracker.get_slot('email_address')
        slot_phone = tracker.get_slot('phone')
        slot_checkin_date = tracker.get_slot('checkin_date')
        slot_checkout_date = tracker.get_slot('checkout_date')
        slot_number_guests = tracker.get_slot('number_guests')
        slot_room_type = tracker.get_slot('room_type')
        slot_reservation_number = tracker.get_slot('reservation_number')
        slot_number_rooms = tracker.get_slot('number_rooms')
      
        # add reservation to client database
        file_operator = mycsvfileoperation.GuestDatabase("clientdatabase.csv")
        a_client = mycsvfileoperation.Client()
        a_client.first_name = slot_first_name
        a_client.last_name = slot_last_name
        a_client.email_address = slot_email_address
        a_client.checkin_date = slot_checkin_date
        a_client.checkout_date = slot_checkout_date
        a_client.number_guests = slot_number_guests
        a_client.number_rooms = slot_number_rooms
        a_client.type_room = slot_room_type
        a_client.reservation_number = slot_reservation_number
        done = file_operator.add_reservation(a_client)

        # book a room and store it a the rooms database
        file_operator2 = mycsvfileoperation.RoomDatabase("roomdatabase.csv")
        a_room1 = mycsvfileoperation.Room()
        a_room1.type_room = slot_room_type
        a_room1.first_name = slot_first_name
        a_room1.last_name = slot_last_name
        a_room1.checkin_date = slot_checkin_date
        a_room1.checkout_date = slot_checkout_date
        a_room1.number_guests = slot_number_guests
        a_room1.reservation_number = slot_reservation_number
        
        if (slot_number_rooms == "1"):
        
            room_no1 = file_operator2.book_one_room(a_room1)
            
        elif (slot_number_rooms == "2"):   
            
             room_no1, room_no2 = file_operator2.book_two_rooms(a_room1)

class ActionCheckAllARoomAvail(Action):
    """
    Check the number of all available rooms
    """
    def name(self) -> Text:
        return "action_check_all_avail_rooms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # check the number of available rooms of type one, two and double
        file_operator2 = mycsvfileoperation.RoomDatabase("roomdatabase.csv")
        no_room_one, no_room_two, no_room_double = file_operator2.read_all_avail_rooms()
        
        return [ SlotSet("no_room_one", no_room_one),SlotSet("no_room_two", no_room_two), SlotSet("no_room_double", no_room_double)]

class ActionCheckRoomAvail(Action):
    """
    Check if the desired room(s) is available
    """
    def name(self) -> Text:
        return "action_check_room_avail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        slot_room_type = tracker.get_slot('room_type')
        slot_checkin_date = tracker.get_slot('checkin_date')
        slot_checkout_date = tracker.get_slot('checkout_date')
        slot_number_guests = tracker.get_slot('number_guests')
        slot_number_rooms = tracker.get_slot('number_rooms')
        
        a_room1 = mycsvfileoperation.Room()
        a_room1.type_room = slot_room_type
        a_room1.checkin_date = slot_checkin_date
        a_room1.checkout_date = slot_checkout_date
        a_room1.number_guests = slot_number_guests
    
        file_operator2 = mycsvfileoperation.RoomDatabase("roomdatabase.csv")
        
        # check only 1 room, if the user request only 1 room
        if (slot_number_rooms == "1"):
            
            room_no1 = file_operator2.check_one_room_avail(a_room1)
            
            # check availability by business logic and data from database
            if (room_no1 == 0):
                    
                dispatcher.utter_message(text=f"Sorry, we have no available room of this type in that time period.")
                    
            else:
                
                dispatcher.utter_message(text=f"Great, we can offer room no. {room_no1}. We charge €60 a night.")
                dispatcher.utter_template("utter_ask_book_room_now", tracker)
        
        # check 2 rooms, if the user request 2 rooms
        elif (slot_number_rooms == "2"):
            
            room_no1, room_no2 = file_operator2.check_two_room_avail(a_room1)
                        
            # check availability by business logic and data from database
            if (room_no1 == 0 or room_no2 == 0):
                    
                dispatcher.utter_message(text=f"Sorry, we have no available room of this type in that time period.")
                dispatcher.utter_template("utter_deny_message", tracker)
                    
            else:
                
                dispatcher.utter_message(text=f"Great, we can offer rooms no. {room_no1} and no. {room_no2}. We charge €60 a night for a person.")
                dispatcher.utter_template("utter_ask_book_room_now", tracker)
            
        return []

class ActionGenerateReserationNumber(Action):
    
    """
    Generate a reservation number
    """
    def name(self):
        return "action_generate_reservation_number"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # generate a unique randmom reservation number with 6 digits
        res_no = random.randrange(100000,999999,1)
        
        return [SlotSet("reservation_number", res_no)]

class ActionCancelReservation(Action):
    """
    Cancel an existing reservation
    """
    def name(self):
        return "action_cancel_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slot_cancel_reservation_number = tracker.get_slot('cancel_reservation_number')
        
        # delete reservation
        file_operator = mycsvfileoperation.GuestDatabase("clientdatabase.csv")
        del_client = mycsvfileoperation.Client()
        del_client.reservation_number = slot_cancel_reservation_number
        done = file_operator.delete_reservation(del_client)
        
        # delete room reservation
        a_room2 = mycsvfileoperation.Room()
        a_room2.reservation_number = tracker.get_slot('cancel_reservation_number')
        file_operator2 = mycsvfileoperation.RoomDatabase("roomdatabase.csv")
        done2 = file_operator2.delete_room_reservation(a_room2)
           
        if done and done2:    
            
            dispatcher.utter_message(text=f"We have canceled the reservation. You receive a confirmation email.")
                
        else:
            
            dispatcher.utter_message(text=f"Havn´t found this reservation.")            
    
        return []

class ValidateTableForm(FormValidationAction):
    """
    Validate the restaurant table time
    """
    def name(self) -> Text:
        return "validate_table_form"

    def validate_restaurant_table_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `restaurant_table_time` value."""

        # check the user input: length of time
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"That's a very short time. I'm assuming you mis-spelled.")
            return {"restaurant_table_time": None}
        else:
            return {"restaurant_table_time": slot_value}

class ActionBookRestaurantTable(Action):
    """
    Book a restaurant table
    """
    def name(self):
        return "action_book_restaurant_table"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             
        
        # book a restaurant table
        file_operator3 = mycsvfileoperation.RestaurantDatabase("restaurantdatabase.csv")
        all_tables = file_operator3.read_data()
        slot_first_name = tracker.get_slot('first_name')
        slot_last_name = tracker.get_slot('last_name')
        slot_checkin_date = tracker.get_slot('checkin_date')
        slot_reservation_time = tracker.get_slot('restaurant_table_time')
        
        if (slot_first_name == None or slot_last_name == None):
             
            dispatcher.utter_message(text=f"Sorry, you have to book a hotel room first.")
            
        else:
        
            a_table =  mycsvfileoperation.Table()
            a_table.first_name = slot_first_name                    # first name of client
            a_table.last_name = slot_last_name                      # last name of client
            a_table.reservation_date = slot_checkin_date            # reservation date
            a_table.reservation_time = slot_reservation_time        # reservation time
            table_no = file_operator3.add_reservation(a_table)
            
            if table_no == 0:    
                
                dispatcher.utter_message(text=f"Sorry, we have available restaurant table.")
                    
            else:
                
                dispatcher.utter_message(text=f"Great, I have booked the restaurant table.")            
    
        return []
    
class CheckClientMessagePreCondition(Action):
    """
    Check the user message
    """
    def name(self):
        return "action_check_message_precondition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        slot_first_name = tracker.get_slot('first_name')
        slot_last_name = tracker.get_slot('last_name')
        
        # if the guest hasn´t booked a room yet, inform the guest to leave the contact details in the message
        if (slot_first_name == None or slot_last_name == None):
            dispatcher.utter_message(text=f"Please don´t forget to leave your contact details.")    
        
        return []

class StoreClientMessage(Action):
    """
    Store the client message in the client message database table
    """
    def name(self):
        return "action_store_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        slot_first_name = tracker.get_slot('first_name')
        slot_last_name = tracker.get_slot('last_name')
        
        # if the guest first and last name is present, attach dem to the message
        if (slot_first_name != None and slot_last_name != None):
            
            slot_client_message = str(slot_first_name) + str(",") + str(slot_last_name)+ str(":")  + tracker.get_slot('client_message')
            
        else:
            slot_client_message = tracker.get_slot('client_message')
        
        # store a client message
        file_operator4 = mycsvfileoperation.MessageDatabase("messagedatabase.csv")
        file_operator4.add_message(slot_client_message)
    
        return []

class ActionBrakfast(Action):
    """
    user ask for a breakfast
    """
    def name(self) -> Text:
        return "action_get_breakfast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_template("utter_breakfast_avail", tracker)
        
        return []
    
class ActionCarParking(Action):
    """
    user asks for a parking place for the car
    """
    def name(self) -> Text:
        return "action_get_carparking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_template("utter_park_place_avail", tracker)

        return []
    
class ActionPaymentslAvail(Action):
    """
    user ask for payment possibilities
    """
    def name(self):
        return "action_payments_avail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_template("utter_payments_avail", tracker)
    
        return []    
    
    
class ActionFitnessAvail(Action):
    """
    user ask for fitness offer
    """
    def name(self):
        return "action_fitness_services_avail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_template("utter_fitness_services_avail", tracker)
        
        return []
    
    
class ActionCheckInOutTimes(Action):
    """
    user ask for check-in and check-out times
    """
    def name(self):
        return "action_checkinout_times"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_template("utter_ask_checkinouttimes", tracker)
        
        return []   

    