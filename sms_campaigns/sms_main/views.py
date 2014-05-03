from sms_main.models import *

def addGroup(group_name):
    Group.objects.create(name=group_name)
    
def addCampaign(name, description, groupId, message_interval, repeats):
    group = Group.objects.get(id=groupId)
    Campaign.objects.create(name=name, description=description, group=group, message_interval_in_seconds=message_interval, total_message_occurrences=repeats)
    
def addRecipient(first_name, last_name, phone_number):
    Recipient.objects.create(first_name=first_name, last_name=last_name, phone_number=phone_number)

