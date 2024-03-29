# Generated by Django 4.0.2 on 2022-10-25 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0011_bot_alter_hit_is_parsed_visitor_hit_visitor'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='asfullname',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='As'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='asname',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='As Name'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='city',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='country',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='countryCode',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='Country Code'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='currency',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='Currency'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='is_parsed',
            field=models.BooleanField(default=False, verbose_name='Is parsed'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='isp',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='ISP'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='mobile',
            field=models.BooleanField(default=False, verbose_name='Is parsed'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='org',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='Org'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='proxy',
            field=models.BooleanField(default=False, verbose_name='Is parsed'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='region',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='Region'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='regionName',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='Region Name'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='timezone',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='Timezone'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='zip',
            field=models.FloatField(blank=True, null=True, verbose_name='Zip'),
        ),
    ]
