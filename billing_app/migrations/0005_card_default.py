# Generated by Django 2.1.7 on 2020-03-17 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing_app', '0004_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='default',
            field=models.BooleanField(default=True),
        ),
    ]
