# Generated by Django 3.2.8 on 2021-10-31 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('miniapp', '0009_auto_20211030_0550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchases',
            name='user_pk',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='miniapp.datepurchase'),
        ),
    ]
