# Generated by Django 5.0 on 2023-12-05 10:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_client_clientid'),
    ]

    operations = [
        migrations.AddField(
            model_name='postservice',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time when the post was created'),
        ),
        migrations.AddField(
            model_name='postservice',
            name='description',
            field=models.TextField(default='', help_text='Description of the service'),
        ),
        migrations.AddField(
            model_name='postservice',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='postservice',
            name='location',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='postservice',
            name='title',
            field=models.CharField(default='', help_text='Title of the service post', max_length=100),
        ),
    ]