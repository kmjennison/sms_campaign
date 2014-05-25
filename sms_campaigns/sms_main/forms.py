from django.forms import ModelForm
from sms_main.models import Campaign
from django import forms

class CampaignForm(ModelForm):
    class Meta:
        model = Campaign
        exclude = ('group',)