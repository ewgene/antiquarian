# Generated by Django 5.1.4 on 2025-06-18 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_productcategory_options_productimage_caption'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=300),
        ),
    ]
