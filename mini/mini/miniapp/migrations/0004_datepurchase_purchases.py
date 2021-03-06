# Generated by Django 3.2.8 on 2021-10-29 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniapp', '0003_cart_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatePurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_pk', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_pk', models.IntegerField()),
                ('product_pk', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
