from django.contrib import admin
from sms_main.models import *

class RecipientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    
class MembershipAdmin(admin.ModelAdmin):
    # Recipient.objects.get(id=recipient)
    list_display = ('recipient', 'campaign', 'time_joined', 'active', 'total_messages_sent')

class CampaignAdmin(admin.ModelAdmin):
    # Recipient.objects.get(id=recipient)
    list_display = ('name', 'group', 'message_text', 'message_interval_in_seconds', 'total_message_occurrences')

admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Group)