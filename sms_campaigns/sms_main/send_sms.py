from twilio.rest import TwilioRestClient

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC9b7ed889c04a5f289279a6ef0d6e341e"
auth_token  = "ba2bb066b9641607e615eb759e7c7e84"
client = TwilioRestClient(account_sid, auth_token)

def sendSMS(number, messageBody):
	message = client.messages.create(body=messageBody,
	    to="+1" + number,    # Replace with your phone number
	    from_="+13312096805") # Replace with your Twilio number
	print message.sid