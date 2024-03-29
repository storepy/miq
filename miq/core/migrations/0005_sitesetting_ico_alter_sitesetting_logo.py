# Generated by Django 4.0.2 on 2022-08-09 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_sitesetting_ico_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='ico',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ico', to='core.file'),
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='logo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='setting', to='core.image', verbose_name='Logo'),
        ),
    ]
