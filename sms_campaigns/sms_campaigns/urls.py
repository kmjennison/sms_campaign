from django.conf.urls import patterns, include, url
from sms_main.views import sms

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sms_campaigns.views.home', name='home'),
    # url(r'^sms_campaigns/', include('sms_campaigns.foo.urls')),
    
    url(r'^$', 'sms_main.views.home', name='home'),
    url(r'^sms/$', sms),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    ### Not currently using.
    # url(r'^campaign/', 'sms_main.views.campaign'),

    url(r'^sms$', sms),

    url(r'^sign_up$', 'sms_main.views.sign_up')
)
