# Generated by Django 5.0 on 2023-12-05 22:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_postservice_date_posted_postservice_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('ProgressID', models.AutoField(primary_key=True, serialize=False)),
                ('Message', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='postservice',
            name='serviceID',
        ),
        migrations.RemoveField(
            model_name='postservice',
            name='workerID',
        ),
        migrations.RemoveField(
            model_name='rateservice',
            name='requestID',
        ),
        migrations.RemoveField(
            model_name='servicerequest',
            name='serviceID',
        ),
        migrations.RemoveField(
            model_name='servicerequest',
            name='clientID',
        ),
        migrations.RemoveField(
            model_name='servicerequest',
            name='workerID',
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('NotificationID', models.AutoField(primary_key=True, serialize=False)),
                ('Message', models.TextField()),
                ('ClientID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.client')),
                ('WorkerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.worker')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('ServiceID', models.AutoField(primary_key=True, serialize=False)),
                ('ServiceName', models.CharField(max_length=255)),
                ('Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('WorkerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.worker')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('TransactionID', models.AutoField(primary_key=True, serialize=False)),
                ('StartStatus', models.CharField(max_length=255)),
                ('CompletedStatus', models.CharField(max_length=255)),
                ('Task', models.CharField(max_length=255)),
                ('ProgressID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.progress')),
                ('ServiceID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.services')),
            ],
        ),
        migrations.AddField(
            model_name='progress',
            name='TransactionID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.transaction'),
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('HistoryID', models.AutoField(primary_key=True, serialize=False)),
                ('TransactionID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.transaction')),
            ],
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='PostService',
        ),
        migrations.DeleteModel(
            name='RateService',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.DeleteModel(
            name='ServiceRequest',
        ),
    ]