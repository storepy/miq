# Generated by Django 3.2.2 on 2021-08-06 16:47

from django.db import migrations, models
import miq.models.image_mod


class Migration(migrations.Migration):

    dependencies = [
        ('miq', '0003_alter_user_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='thumb',
            field=models.ImageField(blank=True, help_text='Select an image file', null=True, upload_to=miq.models.image_mod.upload_thumb_to, verbose_name='Thumbnail'),
        ),
        migrations.AddField(
            model_name='image',
            name='thumb_sq',
            field=models.ImageField(blank=True, help_text='Select an image file', null=True, upload_to=miq.models.image_mod.upload_thumb_to, verbose_name='Square Thumbnail'),
        ),
    ]
