# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC4d790ffece15eb3498000fd049742bb6'
auth_token = '6631b78564a39c05ca3025abe0d1f24b'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Hello! This is a test :)",
                     from_='+12248083800',
                     to='+12533101489'
                 )

print(message.sid)