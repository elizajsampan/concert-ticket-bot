'''Lambda Handler'''
from utils import read_concerts
from utils import read_seat_types
from utils import read_concert_dates
from utils import read_concert_venues
from utils import read_important_details
from utils import send_email
from validators import validate_purchase_ticket_slots
from validators import validate_ticket_guidelines
from validators import validate_available_concerts

CONCERTS = read_concerts()
SEAT_TYPES = read_seat_types()
DATES = read_concert_dates()
VENUES = read_concert_venues()
DETAILS = read_important_details()


def lambda_handler(event, context):
    """Lambda handler"""
    # print(event)
    this_handler = Handler(event)
    print(context)
    return this_handler.process()

# pylint: disable=too-many-instance-attributes


class Handler:
    """Handler for lambda events"""

    def __init__(self, event):
        """Initializer"""
        self.intent_type = "Close"
        self.state = "Fulfilled"
        self.slot_to_elicit = None
        self.session_attributes = None
        self.answer_attributes = None
        self.messages = []
        self.contexts = []
        self.event = event
        self.session = event['sessionState']
        self.current_intent = self.session['intent']['name']
        self.slots = self.session['intent']['slots']
        self.invocation_source = event['invocationSource']
        self.buttons = []
        self.email = ''

    def create_buttons(self):
        '''Create buttons for response card'''
        buttons = []
        for button in self.buttons:
            button_text = {
                "text": button,
                "value": button
            }
            buttons.append(button_text)
        # print(buttons)
        return buttons

    def generate_plaintext_message(self, message):
        '''Generate plaintext for response'''
        plaintext_message = {
            "contentType": "PlainText",
            "content": message
        }
        self.messages.append(plaintext_message)

    def generate_response_card(self, title, subtitle):
        '''Generate response card for response'''
        response_card = {
            "contentType": "ImageResponseCard",
            "imageResponseCard": {
                "title": title,
                "subtitle": subtitle,
                "buttons": self.create_buttons()
            }
        }
        return response_card

    def process_initial_intent(self):
        """InitialIntent Fulfillment"""
        self.current_intent = "InitialIntent"
        content = "Hi! How may I help you?"
        self.generate_plaintext_message(content)
        btn1 = "I want to se the available concerts"
        btn2 = "I want to see the ticket and purchase guidelines"
        btn3 = "I want to buy a concert ticket"
        self.buttons = [btn1, btn2, btn3]
        title = "I can help you with the following"
        subtitle = "(You may want to ask...)"
        card = self.generate_response_card(title, subtitle)
        self.messages.append(card)

    def process_fallback_intent(self):
        """FallbackIntent Fulfillment"""
        self.current_intent = "FallbackIntent"
        content = "Sorry I didn't catch that"
        self.generate_plaintext_message(content)
        btn1 = "I want to see the available concerts"
        btn2 = "I want to see the ticket and purchase guidelines"
        btn3 = "I want to buy a concert ticket"
        self.buttons = [btn1, btn2, btn3]
        title = "I can help you with the following"
        subtitle = "(You may want to ask...)"
        card = self.generate_response_card(title, subtitle)
        self.messages.append(card)

    def process_purchase_ticket_intent(self):
        """Processes PurchaseTicketIntent in FulfillmentCodeHook"""
        self.current_intent = "PurchaseTicketIntent"
        concert = self.slots["Concerts"]["value"]["interpretedValue"]
        seat_type = self.slots["SeatType"]["value"]["interpretedValue"]
        email = self.slots["ContactDetails"]["value"]["interpretedValue"]
        date = DATES.get('concerts_dates').get(concert)
        venue = VENUES.get('concert_venues').get(concert)
        concert_str = f"Your purchase of {seat_type} been confirmed. " + concert
        date_str = " Concert is on " + date
        venue_str = " at 7pm. It will be held on " + venue
        content = concert_str + date_str + venue_str
        send_email(email, content)
        self.generate_plaintext_message(str(content))

    def process_ticket_purchase_guidelines_intent(self):
        """Processes TicketPurchaseGuidelinesIntent in FulfillmentCodeHook"""
        self.current_intent = "TicketPurchaseGuidelinesIntent"
        details = self.slots["Details"]["value"]["interpretedValue"]
        content = DETAILS.get('important_details').get(details)
        self.generate_plaintext_message(content)

    def process_available_concerts_intent(self):
        """Processes AvailableConcertsIntent in FulfillmentCodeHook"""
        self.current_intent = "AvailableConcertsIntent"
        concert = self.slots["ConcertDetails"]["value"]["interpretedValue"]
        date = DATES.get('concerts_dates').get(concert)
        venue = VENUES.get('concert_venues').get(concert)
        content = concert + " Concert is on " + date + \
            " at 7pm. It will be held on " + venue
        self.generate_plaintext_message(str(content))

    def fulfill_intent(self):
        """Calls function for FulfillmentCodeHook"""
        if self.current_intent == "InitialIntent":
            self.process_initial_intent()
        if self.current_intent == "PurchaseTicketIntent":
            self.process_purchase_ticket_intent()
        if self.current_intent == "TicketPurchaseGuidelinesIntent":
            self.process_ticket_purchase_guidelines_intent()
        if self.current_intent == "AvailableConcertsIntent":
            self.process_available_concerts_intent()
        if self.current_intent == "FallbackIntent":
            self.process_fallback_intent()

    def process(self):
        """Processes Lex intents above"""
        validation_response = ""

        if self.current_intent == "PurchaseTicketIntent":
            validation_response = validate_purchase_ticket_slots(self.slots)

        if self.current_intent == "TicketPurchaseGuidelinesIntent":
            validation_response = validate_ticket_guidelines(self.slots)

        if self.current_intent == "AvailableConcertsIntent":
            validation_response = validate_available_concerts(self.slots)

        if self.invocation_source == "DialogCodeHook":
            if not validation_response['isValid']:
                if "message" in validation_response:
                    self.slot_to_elicit = validation_response["violatedSlot"]
                    self.intent_type = "ElicitSlot"
                    text = validation_response["message"]
                    self.generate_plaintext_message(text)
                else:
                    self.intent_type = "ElicitSlot"
                    self.slot_to_elicit = validation_response["violatedSlot"]
            else:
                self.intent_type = "Delegate"
            return self.generate_response()

        if self.invocation_source == "FulfillmentCodeHook":
            self.fulfill_intent()
            return self.generate_response()

        return None

    def generate_response(self):
        """Generates response to be sent to Lex"""
        response = {
            "sessionState": {
                "dialogAction": {
                    "slotToElicit": self.slot_to_elicit,
                    "type": self.intent_type,
                },
                "intent": {
                    "name": self.current_intent,
                    "slots": self.slots,
                    "state": self.state
                }
            },
            "messages": self.messages
        }

        return response
