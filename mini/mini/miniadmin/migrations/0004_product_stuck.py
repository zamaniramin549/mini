# Generated by Django 3.2.8 on 2021-10-25 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniadmin', '0003_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stuck',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]