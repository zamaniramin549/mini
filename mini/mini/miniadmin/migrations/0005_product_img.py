# Generated by Django 3.2.8 on 2021-10-25 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniadmin', '0004_product_stuck'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]