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
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('phone_number', self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128, unique=True, null=True, blank=True)),
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
            ('time_last_received_message', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('last_received_message', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('no_response_contact', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
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
            ('no_response_action', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'sms_main', ['Campaign'])

        # Adding model 'Responses'
        db.create_table(u'sms_main_responses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.BigIntegerField')()),
            ('enrollee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sms_main.Recipient'])),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sms_main.Campaign'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'sms_main', ['Responses'])

        # Adding model 'Group'
        db.create_table(u'sms_main_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ein', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('isActive', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'sms_main', ['Group'])

        # Adding model 'UserProfile'
        db.create_table(u'sms_main_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sms_main.Group'], null=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sms_main.Campaign'], null=True, blank=True)),
            ('phone_number', self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128, null=True, blank=True)),
            ('permitted_enroller', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'sms_main', ['UserProfile'])


    def backwards(self, orm):
        # Deleting model 'Recipient'
        db.delete_table(u'sms_main_recipient')

        # Deleting model 'Membership'
        db.delete_table(u'sms_main_membership')

        # Deleting model 'Campaign'
        db.delete_table(u'sms_main_campaign')

        # Deleting model 'Responses'
        db.delete_table(u'sms_main_responses')

        # Deleting model 'Group'
        db.delete_table(u'sms_main_group')

        # Deleting model 'UserProfile'
        db.delete_table(u'sms_main_userprofile')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sms_main.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms_main.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_interval_in_seconds': ('django.db.models.fields.BigIntegerField', [], {}),
            'message_text': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'no_response_action': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'no_response_timeout_in_seconds': ('django.db.models.fields.BigIntegerField', [], {}),
            'response_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_message_occurrences': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'sms_main.group': {
            'Meta': {'object_name': 'Group'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ein': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'sms_main.membership': {
            'Meta': {'object_name': 'Membership'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms_main.Campaign']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_received_message': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'no_response_contact': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms_main.Recipient']"}),
            'time_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_last_received_message': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_last_sent_message': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'total_messages_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'sms_main.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'campaigns': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sms_main.Campaign']", 'through': u"orm['sms_main.Membership']", 'symmetrical': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'sms_main.responses': {
            'Meta': {'object_name': 'Responses'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms_main.Campaign']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'enrollee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms_main.Recipient']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'sms_main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms_main.Campaign']", 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms_main.Group']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permitted_enroller': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_number': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['sms_main']