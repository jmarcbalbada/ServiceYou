# Generated by Django 5.0 on 2023-12-06 08:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_transaction_completedstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='ProgressID',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.progress'),
        ),
    ]