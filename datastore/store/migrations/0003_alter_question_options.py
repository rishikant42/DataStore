# Generated by Django 4.0.6 on 2022-07-10 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_question_date_format_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.ManyToManyField(default=[], to='store.questionoption'),
        ),
    ]
