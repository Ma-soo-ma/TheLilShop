# Generated by Django 5.2 on 2025-05-05 10:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_customer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(choices=[('Lahore', 'Lahore'), ('Karachi', 'Karachi'), ('Islamabad', 'Islamabad'), ('Peshawar', 'Peshawar'), ('Quetta', 'Quetta'), ('Rawalpindi', 'Rawalpindi'), ('Faisalabad', 'Faisalabad'), ('Multan', 'Multan'), ('Gujranwala', 'Gujranwala'), ('Gujrat', 'Gujrat'), ('Sialkot', 'Sialkot'), ('Sukkur', 'Sukkur'), ('Hyderabad', 'Hyderabad'), ('Nawabshah', 'Nawabshah'), ('Mirpurkhas', 'Mirpurkhas')], max_length=200),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
