# Generated by Django 3.0.5 on 2020-04-23 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question_and_answer', '0002_auto_20200422_2015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='accepted',
            new_name='right',
        ),
    ]