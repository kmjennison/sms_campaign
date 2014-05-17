# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Recipient'
        db.create_table(u'sms_main_recipient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'sms_main', ['Recipient'])

        # Adding model 'Membership'
        db.create_table(u'sms_main_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sms_main.Recipient'])),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sms_main.Campaign'])),
            ('time_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('time_last_sent_message', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('total_messages_sent', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('time_last_received_message', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('last_received_message', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('no_response_contact', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'sms_main', ['Membership'])

        # Adding model 'Campaign'
        db.create_table(u'sms_main_campaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sms_main.Group'])),
            ('message_interval_in_seconds', self.gf('django.db.models.fields.BigIntegerField')()),
            ('total_message_occurrences', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('message_text', self.gf('django.db.models.fields.TextField')()),
            ('response_requested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_response_timeout_in_seconds', self.gf('django.db.models.fields.BigIntegerField')()),
            ('no_response_action', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'sms_main', ['Campaign'])

        # Adding model 'Group'
        db.create_table(u'sms_main_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sms_main', ['Group'])


    def backwards(self, orm):
        # Deleting model 'Recipient'
        db.delete_table(u'sms_main_recipient')

        # Deleting model 'Membership'
        db.delete_table(u'sms_main_membership')

        # Deleting model 'Campaign'
        db.delete_table(u'sms_main_campaign')

        # Deleting model 'Group'
        db.delete_table(u'sms_main_group')


    models = {
        u'sms_main.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms_main.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_interval_in_seconds': ('django.db.models.fields.BigIntegerField', [], {}),
            'message_text': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'no_response_action': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'no_response_timeout_in_seconds': ('django.db.models.fields.BigIntegerField', [], {}),
            'response_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_message_occurrences': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'sms_main.group': {
            'Meta': {'object_name': 'Group'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'sms_main.membership': {
            'Meta': {'object_name': 'Membership'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms_main.Campaign']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_received_message': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'no_response_contact': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms_main.Recipient']"}),
            'time_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_last_received_message': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'time_last_sent_message': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'total_messages_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'sms_main.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'campaigns': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sms_main.Campaign']", 'through': u"orm['sms_main.Membership']", 'symmetrical': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['sms_main']