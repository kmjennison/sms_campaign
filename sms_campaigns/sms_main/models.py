from django.db import models
from datetime import datetime

class Recipient(models.Model):
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
    
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=30)
    campaigns = models.ManyToManyField('Campaign', through='Membership')

class Membership(models.Model):
    def __unicode__(self):
        return str(self.id)
    recipient = models.ForeignKey(Recipient)
    campaign = models.ForeignKey('Campaign')
    time_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    time_last_sent_message = models.DateTimeField(default=datetime.now)
    total_messages_sent = models.IntegerField(default=0)
    time_last_received_message = models.DateTimeField(default=datetime.now)
    last_received_message = models.CharField(max_length=256)
    no_response_contact = models.CharField(max_length=30)

class Campaign(models.Model):
    def __unicode__(self):
        return self.name
    
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    group = models.ForeignKey('Group')
    message_interval_in_seconds = models.BigIntegerField()
    total_message_occurrences = models.IntegerField(default=1)
    message_text = models.TextField()
    response_requested = models.BooleanField(default=False)
    no_response_timeout_in_seconds = models.BigIntegerField()
    no_response_action = models.CharField(max_length=256)
    
class Group(models.Model):
    def __unicode__(self):
        return self.name
    
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)