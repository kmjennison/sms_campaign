from sms_main.models import *
import time
from datetime import datetime
import pytz
from twilio.rest import TwilioRestClient
from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from django.conf import settings


def addGroup(group_name):
    Group.objects.create(name=group_name)
    
def addCampaign(name, description, groupId, message_interval, repeats):
    group = Group.objects.get(id=groupId)
    Campaign.objects.create(name=name, description=description, group=group, message_interval_in_seconds=message_interval, total_message_occurrences=repeats)
    
def addRecipient(first_name, last_name, phone_number):
    Recipient.objects.create(first_name=first_name, last_name=last_name, phone_number=phone_number)

def addRecipientToGroup(recipientId, groupId):
    recip = Recipient.objects.get(id=recipientId)
    group = Group.objects.get(id=groupId)
    m = Membership(recipient=recip, group=group)
    m.save()
    
# Returns seconds that have elapsed between datetime and now.
def timeElapsed(datetime):
    now = datetime.utcnow().replace(tzinfo = pytz.utc)
    td = now - datetime
    return td.seconds

# See if enough time has elapsed for a new message.
# "time_last_sent_message" is the datetime we last sent the recipient a message.
# "messaging_inteval" is how often the campaign messages people.
def shouldSendMessage(time_last_sent_message, messaging_interval):
    seconds_since_last_message = timeElapsed(time_last_sent_message)
    if messaging_interval < seconds_since_last_message:
        return True
    return False

# For every membership (recipient/campaign combination), check to see if it's time to send the user a message.
def checkToSendMessages():
    memberships = Membership.objects.filter(active=True)
    for m in memberships:
        if shouldSendMessage(m.time_last_sent_message, m.campaign.message_interval_in_seconds):
            sendMessage(m.recipient.phone_number, m.campaign.message_text)
            m.time_last_sent_message = datetime.utcnow().replace(tzinfo = pytz.utc)
            m.total_messages_sent += 1
            # If we've sent all our text messages, make the membership inactive.
            if m.total_messages_sent >= m.campaign.total_message_occurrences:
                m.active = False
            m.save()
            
def sendMessage(phone_number, messageBody):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token  = settings.TWILIO_AUTH_TOKEN
    client = TwilioRestClient(account_sid, auth_token)

    # hard code this in for now
    # phone_number = "4155833353"
    # messageBody = "Ahoy from the sms campaign!"

    message = client.messages.create(body=messageBody,
        to="+1" + phone_number, 
        from_="+13312096805")
    print "Sending message to " + phone_number + ": " + messageBody

@twilio_view
def sms(request):
    enrolleeNumber = request.POST.get('Body', '')
    msg = 'Enrollment for %s confirmed' % (enrolleeNumber)
    r = Response()
    r.message(msg)
    enrollmentMessage = 'You have been enrolled in this progam. Stay tuned!'
    sendMessage(enrolleeNumber, enrollmentMessage)
    return r