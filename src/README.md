#### ConcertTicketBot-Function (Amazon Lambda)

--py--

Python version 3.9

lambda_function.py: (main) contains lambda handler events

utils.py: reads json files, imported by lambda_function and validators

validators.py: validates slots, imported by lambda_function

keys.py: contains credentials for SMTP

<br>

--json--

available_concerts.json: contains available concert artists

concert_dates.json: contains concert date per concert artist

concert_venue.json: contains concert venur per concert artist

important_details: contains important details (concert reminders)

seat_types.json: containts seat types

seat_count.json: contains available seats (count) per seat type


