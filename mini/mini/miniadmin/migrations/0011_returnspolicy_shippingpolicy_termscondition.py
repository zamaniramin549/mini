# Generated by Django 3.2.8 on 2021-11-03 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniadmin', '0010_qaa'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnsPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TermsCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]