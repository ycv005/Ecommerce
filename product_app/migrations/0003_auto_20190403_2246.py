# Generated by Django 2.1.2 on 2019-04-03 17:16

from django.db import migrations, models
import product_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to=product_app.models.user_directory_path),
        ),
    ]
