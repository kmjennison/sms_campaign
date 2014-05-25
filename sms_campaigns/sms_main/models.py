from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField

class Recipient(models.Model):
    def __unicode__(self):
        return str(self.phone_number) + ': ' + self.first_name + ' ' + self.last_name
    
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
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
    time_last_received_message = models.DateTimeField(default=datetime.now, null=True, blank=True)
    last_received_message = models.CharField(max_length=256, null=True, blank=True)
    no_response_contact = models.CharField(max_length=30, null=True, blank=True)

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
    ein = models.CharField(blank=True, max_length=256)
    isActive = models.BooleanField(default=False)

class UserProfile(models.Model):
    def __unicode__(self):
        return str(self.user)

    user = models.OneToOneField(User)
    group = models.ForeignKey('Group', null=True)
    campaign = models.ForeignKey('Campaign', null=True, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True, help_text="Format this as +1234567890.")
    permitted_enroller = models.BooleanField(default=False, verbose_name="This person is allowed to enroll people in campaigns via text.")

# does this get called at the time of user creation...???
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)