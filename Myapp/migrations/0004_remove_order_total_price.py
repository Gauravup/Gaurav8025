# Generated by Django 5.0.1 on 2024-03-13 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0003_watch_percentage_watch_price_and_quantity_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
    ]