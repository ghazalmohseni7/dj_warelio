# Generated by Django 5.2.1 on 2025-05-21 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_request', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockrequest',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
