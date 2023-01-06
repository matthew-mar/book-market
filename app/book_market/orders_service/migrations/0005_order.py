# Generated by Django 4.1.5 on 2023-01-06 09:38

import common.utils
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders_service', '0004_bookset_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField()),
                ('number', models.BigIntegerField(default=common.utils.big_int, unique=True)),
                ('address', models.TextField(max_length=50)),
                ('set_id', models.UUIDField(unique=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('delivery_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders_service.deliverymethod')),
                ('payment_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders_service.paymethod')),
            ],
        ),
    ]