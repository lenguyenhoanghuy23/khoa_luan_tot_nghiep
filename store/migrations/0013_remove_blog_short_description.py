# Generated by Django 3.2.9 on 2022-01-16 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_contact_date_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='short_description',
        ),
    ]