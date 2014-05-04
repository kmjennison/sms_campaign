import send_sms

# a simple sample function to call test the send_sms.py functionality
# change the number to something else to text yourself

number = "4155833353"
messageBody = "Hello from sms_campaign!"

send_sms.sendSMS(number, messageBody)