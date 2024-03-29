# Generated by Django 4.0.6 on 2022-07-16 14:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AddField(
            model_name='actionauthconfig',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.CreateModel(
            name='GsheetAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sheet_name', models.CharField(max_length=1024)),
                ('sheet_id', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auth_config', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='action.actionauthconfig')),
            ],
            options={
                'db_table': 'googlesheetaction',
            },
        ),
    ]
