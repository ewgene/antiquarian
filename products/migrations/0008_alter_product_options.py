# Generated by Django 5.1.4 on 2025-07-02 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_fix_duplicate_slugs'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-created_at',), 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]
