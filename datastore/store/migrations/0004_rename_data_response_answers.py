# Generated by Django 4.0.6 on 2022-07-10 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_question_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='response',
            old_name='data',
            new_name='answers',
        ),
    ]
