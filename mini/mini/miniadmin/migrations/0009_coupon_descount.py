# Generated by Django 3.2.8 on 2021-10-29 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniadmin', '0008_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='descount',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
