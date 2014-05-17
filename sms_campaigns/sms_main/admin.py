from django.contrib import admin
from sms_main.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class RecipientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    
class MembershipAdmin(admin.ModelAdmin):
    # Recipient.objects.get(id=recipient)
    list_display = ('recipient', 'campaign', 'time_joined', 'active', 'total_messages_sent')

class CampaignAdmin(admin.ModelAdmin):
    # Recipient.objects.get(id=recipient)
    list_display = ('name', 'group', 'message_text', 'message_interval_in_seconds', 'total_message_occurrences')

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Group)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
