# Generated by Django 5.0.4 on 2024-05-27 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
    ]
