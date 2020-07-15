# Generated by Django 2.2.12 on 2020-04-30 00:10

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import jsonlight


def convert_kwargs(apps, schema_editor):
    Caller = apps.get_model('djcall', 'Caller')
    for caller in Caller.objects.all():
        caller.kwargs = jsonlight.dumps(caller.old_kwargs)
        caller.save()


class Migration(migrations.Migration):

    dependencies = [
        ('djcall', '0003_status_canceled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='caller',
            old_name='kwargs',
            new_name='old_kwargs',
        ),
        migrations.AddField(
            model_name='caller',
            name='kwargs',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.RunPython(convert_kwargs),
    ]
