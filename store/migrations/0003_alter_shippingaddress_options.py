# Generated by Django 4.2.5 on 2023-11-16 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_shippingaddress_options_alter_status_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shippingaddress',
            options={'ordering': ['-date_added'], 'verbose_name': 'Shipping address', 'verbose_name_plural': 'Shipping addresses'},
        ),
    ]
