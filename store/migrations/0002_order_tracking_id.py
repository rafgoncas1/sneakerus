# Generated by Django 4.2.7 on 2023-11-19 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tracking_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
