# Generated by Django 4.0.2 on 2022-08-17 14:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_sitesetting_ico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='meta_slug',
            field=models.SlugField(default=uuid.uuid4, max_length=500, unique=True),
        ),
    ]
