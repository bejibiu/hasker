# Generated by Django 3.0.5 on 2020-05-01 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question_and_answer', '0004_auto_20200425_2013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='right',
            new_name='correct',
        ),
    ]
