# Generated by Django 4.0.2 on 2022-08-09 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_sitesetting_ico_alter_sitesetting_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesetting',
            name='ico',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ico', to='core.file', verbose_name='Favicon link'),
        ),
    ]
