# Generated by Django 3.2.8 on 2021-10-29 21:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('miniapp', '0004_datepurchase_purchases'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='date_purchase_pk',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
