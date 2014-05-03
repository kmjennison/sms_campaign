# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Campaign.message_text'
        db.add_column(u'sms_main_campaign', 'message_text',
                      self.gf('django.db.models.fields.TextField')(default="Don't forget to take your medication every hour."),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Campaign.message_text'
        db.delete_column(u'sms_main_campaign', 'message_text')


    models = {
        u'sms_main.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms_main.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_interval_in_seconds': ('django.db.models.fields.BigIntegerField', [], {}),
            'message_text': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
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
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms_main.Recipient']"}),
            'time_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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