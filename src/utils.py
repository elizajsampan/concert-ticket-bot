'''Get Data '''
import json
import smtplib


def read_concerts():
    '''Get available concerts'''
    with open("available_concerts.json", 'r', encoding="utf-8") as data_file:
        return json.load(data_file)

def read_seat_types():
    '''Get seat types'''
    with open("seat_types.json", 'r', encoding="utf-8") as data_file:
        return json.load(data_file)

def read_concert_dates():
    '''Get concert dates'''
    with open("concert_dates.json", 'r', encoding="utf-8") as data_file:
        return json.load(data_file)

def read_concert_venues():
    '''Get concert venue'''
    with open("concert_venues.json", 'r', encoding="utf-8") as data_file:
        return json.load(data_file)

def read_important_details():
    '''Get important details'''
    with open("important_details.json", 'r', encoding="utf-8") as data_file:
        return json.load(data_file)

def send_email(email, message):
    '''Send email to the provided email'''
    sender_email = 'purchase.success.elli@gmail.com'
    receiver_email = email
    password = 'ddghovcfxovjssxt'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    print("Email has been sent to", receiver_email)
