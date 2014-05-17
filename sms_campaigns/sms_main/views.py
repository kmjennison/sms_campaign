from sms_main.models import *
import time
from datetime import datetime
import pytz
from twilio.rest import TwilioRestClient
from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from django.conf import settings
from sms_campaigns import local_settings
from forms import *
from django.shortcuts import render
from django.template import Context, Template

def addGroup(group_name):
    Group.objects.create(name=group_name)
    
def addCampaign(name, description, groupId, message_interval, repeats, message, no_response_timeout_in_seconds, no_response_action):
    group = Group.objects.get(id=groupId)
    Campaign.objects.create(name=name, description=description, group=group, message_interval_in_seconds=message_interval, total_message_occurrences=repeats, message_text=message, no_response_timeout_in_seconds=no_response_timeout_in_seconds, no_response_action=no_response_action)
    
def addRecipient(first_name, last_name, phone_number):
    Recipient.objects.get_or_create(first_name=first_name, last_name=last_name, phone_number=phone_number)

def addRecipientToCampaign(phone_number, campaignId, no_response_contact):
    recip = Recipient.objects.get(phone_number=phone_number)
    camp = Campaign.objects.get(id=campaignId)

    m = Membership(recipient=recip, campaign=camp, no_response_contact=no_response_contact)
    m.save()
    
def updateEnrolleeResponse(phone_number, message):
    recip = Recipient.objects.get(phone_number=phone_number)
    camp = Campaign.objects.get(id=campaignId)

    m = Membership(recipient=recip, time_last_received_message=datetime.now, last_received_message=message)
    m.save()

def shouldTakeNoResponseAction(time_last_received_message, no_response_timeout):
    seconds_since_last_message = timeElapsed(time_last_received_message)
    if seconds_since_last_message >= no_response_timeout:
        return True
    return False

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

        if shouldTakeNoResponseAction(m.time_last_received_message, m.campaign.no_response_timeout_in_seconds):
            message = "Please call " + m.recipient.phone_number + " and follow-up about " + m.campaign.name
            sendMessage(m.no_response_contact, message)

# putting this here for now, may want to move it to a different file
def isAuthorizedEnroller(phone_number):
    # pseudocode-y
    user = Users.objects.get(phone_number=phone_number)
    userProfile = user.get_profile()

    return userProfile.isAuthorizedEnroller

def isEnrollee(phone_number):
    recip = Recipient.objects.get(phone_number=phone_number)
    if recip:
        return True
        
    return False

def isCampaignCreator(phone_number):
    # pseudocode-y
    user = Users.objects.get(phone_number=phone_number)
    userProfile = user.get_profile()

    return userProfile.isGroupManager

def getGroupByPhoneNumber(phone_number):
    # pseudocode-y
    user = Users.objects.get(phone_number=phone_number)
    userProfile = user.get_profile()

    return userProfile.group

def getCampaignByPhoneNumber(phone_number):
    # pseudocode-y
    user = Users.objects.get(phone_number=phone_number)
    userProfile = user.get_profile()

    return userProfile.campaign

def isValidCampaignID(campaign_id):

    # pull campaign info
    group = Group.objects.get(id=1)
    camps = group.campaign_set.all()

    campaign_ids = [];
    for camp in camps:
        campaign_ids.append(camp.id)
    
    if campaign_id in campaign_ids:
        return True
    else:
        return False

def isPhoneNumber(num_string):
    return len(num_string) == 10

def sendMessage(phone_number, messageBody):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token  = local_settings.TWILIO_AUTH_TOKEN
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(body=messageBody,
        to="+1" + phone_number, 
        from_="+13312096805")
    print "Sending message to " + phone_number + ": " + messageBody

@twilio_view
def sms(request):
    senderNumber = request.POST.get('From', '')

    if isAuthorizedEnroller(senderNumber):
        smsMessage = request.POST.get('Body', '')

        if isPhoneNumber(smsMessage):
            enrolleeNumber = smsMessage

            # store the enrollee phone number in the session for use in between requests
            request.session[senderNumber] is enrolleeNumber

            addRecipient('J', 'Doe', enrolleeNumber)

            # pull campaign info
            group = Group.objects.get(id=1)
            camps = group.campaign_set.all()
            campaignIDs = ''

            for camp in camps:
                campID = str(camp.id)
                campName = camp.name
                campaignIDs = campaignIDs + '\n' + campID + ' - ' + campName

            msg = 'Please select a campaign:\n %s' % (campaignIDs)
            r = Response()
            r.message(msg)

            if enrolleeNumber == local_settings.ALYSON_NUMBER:
                sendMessage(enrolleeNumber, "Hey girl, fork me on Github. - Ryan")
            return r

        else:
            campaignID = int(smsMessage)
            if isValidCampaignID(campaignID) and request.session[senderNumber] != None:
                campaignName = Campaign.objects.get(id=campaignID)
                enrolleeNumber = request.session[senderNumber]

                addRecipientToCampaign(enrolleeNumber, campaignID, senderNumber)
                msg = 'Enrollment in %s confirmed for %s' % (campaignName, enrolleeNumber)
                r = Response()
                r.message(msg)
                enrollmentMessage = 'You have been enrolled for %s. Stay tuned!' % (campaignName)
                sendMessage(enrolleeNumber, enrollmentMessage)
                request.session[senderNumber] = None
                return r

            else:
                msg = 'Invalid request!'
                r = Response()
                r.message(msg)
                return r

    elif isEnrollee(senderNumber):
        enrolleeNumber = senderNumber
        enrolleeMessage = request.POST.get('Body', '')
        updateEnrolleeResponse(enrolleeNumber, enrolleeMessage)

        msg = 'Thanks for the update!'
        r = Response()
        r.message(msg)
        request.session[senderNumber] = None
        return r

    elif isCampaignCreator(senderNumber):
        message = request.POST.get('Body', '')

        if message.upper() == "NEW":
            msg = "Creating new Campaign - Please respond with campaign name"
            r = Response()
            r.message(msg)
            request.session['currField' + senderNumber] = 'name'
            return r
        elif request.session['currField' + senderNumber] == 'name':
            request.session['name' + senderNumber] = message
            msg = "Please respond with campaign description or say 'None' to leave blank"
            r = Response()
            r.message(msg)
            request.session['currField' + senderNumber] = 'description'
            return r
            
        elif request.session['currField' + senderNumber] == 'description':
            request.session['description' + senderNumber] = message
            msg = "Please respond with number of messages to send in campaign"
            r = Response()
            r.message(msg)
            request.session['currField' + senderNumber] = 'numMessage'
            return r
            
        elif request.session['currField' + senderNumber] == 'numMessage':
            request.session['repeats' + senderNumber] = int(message)
            msg = "Please respond with message interval (e.g. '1 day' for once daily)"
            r = Response()
            r.message(msg)
            request.session['currField' + senderNumber] = 'msgInterval'
            return r
            
        elif request.session['currField' + senderNumber] == 'msgInterval':
            message = message.split(' ')
            numeric_frequency = int(message[0])
            str_frequency = message[1]
            multiplier = 3600

            if 'day' in str_frequency:
                multiplier = 86400
            elif 'week' in str_frequency:
                multiplier = 604800
            elif 'month' in str_frequency:
                multiplier = 2.63e+6
            else:
                multiplier = 3600

            message_interval = numeric_frequency * multiplier

            request.session['currField' + senderNumber] = 'message'
            request.session['msgInterval' + senderNumber] = message_interval
            
            msg = "Please respond with message you'd like to send out"
            r = Response()
            r.message(msg)
            return r

        elif request.session['currField' + senderNumber] == 'message':
            name = request.session['name' + senderNumber]
            description = request.session['description' + senderNumber]
            if description is 'None':
                description = None
            repeats = request.session['repeats' + senderNumber]
            groupId = getGroupByPhoneNumber(senderNumber)
            message_interval = request.session['msgInterval' + senderNumber]

            no_response_timeout_in_seconds = '1'
            no_response_action = 'None'

            addCampaign(name, description, groupId, message_interval, repeats, message, no_response_timeout_in_seconds, no_response_action)
            msg = "New campaign successfully created"
            r = Response()
            r.message(msg)

            request.session['currField'] = None
            request.session['name'] = None
            request.session['description'] = None
            request.session['repeats'] = None
            return r
        
        else:
            msg = 'Invalid request'
            request.session['currField'] = None
            request.session['name'] = None
            request.session['description'] = None
            request.session['repeats'] = None
            r = Response()
            r.message(msg)

            return r

    else:
        msg = "Hello! We don't know you yet!"
        r = Response()
        r.message(msg)
        request.session[senderNumber] = None
        return r

def campaign(request):
    form = CampaignForm()
    if request.method == 'POST':
        form = CampaignForm(request.POST)
    else:
        form = CampaignForm()

    return render(request, 'campaign.html', {'form': form})