# Generated by Django 4.0.6 on 2022-07-10 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='date_format',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='lower_limit',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='time_format',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='upper_limit',
            field=models.FloatField(null=True),
        ),
    ]
