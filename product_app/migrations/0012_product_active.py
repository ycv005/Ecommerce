# Generated by Django 2.1.7 on 2019-10-24 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0011_product_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
