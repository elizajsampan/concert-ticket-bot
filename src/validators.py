'''Validators for each Slots'''
from utils import read_concerts, read_seat_types, read_important_details

CONCERTS = read_concerts()
SEAT_TYPES = read_seat_types()
DETAILS = read_important_details()

def generate_validation_response(is_valid, invalid_slot):
    '''Create a vailation response'''
    response = {
    		"isValid": is_valid,
    		"violatedSlot": invalid_slot,
    	  }
    return response

def generate_validation_response_msg(is_valid, invalid_slot, message):
    '''Get validation response message'''
    return {
            "isValid": is_valid,
            "violatedSlot": invalid_slot,
            "message": message
            }

def validate_purchase_ticket_slots(slots):
    '''Validate each slot in PurchaseTicketIntent'''
    if not slots['Concerts']:
        return generate_validation_response(False, "Concerts")
    concerts = CONCERTS.get('available_concerts')
    if slots['Concerts']['value']['originalValue'].lower() not in concerts:
        user_input = slots["Concerts"]["value"]["originalValue"]
        msg = f"\'{user_input}\' concert is not available."
        return generate_validation_response_msg(False, "Concerts", msg)
    if not slots['SeatType']:
        return generate_validation_response(False, "SeatType")
    if slots['SeatType']['value']['originalValue'].lower() not in SEAT_TYPES.get('seat_types'):
        print(SEAT_TYPES.get('seat_types'))
        user_input = slots["SeatType"]["value"]["originalValue"]
        msg = f"\'{user_input}\' seat is not available."
        return generate_validation_response_msg(False, "SeatType", msg)
    if not slots['ContactDetails']:
        return generate_validation_response(False, "ContactDetails")

    return {"isValid": True}

def validate_ticket_guidelines(slots):
    '''Validate each slot in TicketPurchaseGuidelinesIntent'''
    if not slots['Details']:
        return generate_validation_response(False, "Details")

    if slots['Details']['value']['originalValue'].lower() not in DETAILS.get('important_details'):
        user_input = slots["Details"]["value"]["originalValue"]
        msg = f"No details regarding \'{user_input}\'. Please choose from the menu."
        return generate_validation_response_msg(False, "Details", msg)

    return {'isValid': True}

def validate_available_concerts(slots):
    '''Validate each slot in AvailableConcertsIntent'''
    if not slots['ConcertDetails']:
        return generate_validation_response(False, "ConcertDetails")
    concerts = CONCERTS.get('available_concerts')
    if slots['ConcertDetails']['value']['originalValue'].lower() not in concerts:
        print(CONCERTS.get('available_concerts'))
        user_input = slots["ConcertDetails"]["value"]["originalValue"]
        print(user_input)
        msg = f"No details regarding \'{user_input}\' concert. Please choose from the menu."
        return generate_validation_response_msg(False, "ConcertDetails", msg)

    return {'isValid': True}
