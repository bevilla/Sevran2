# Generated by Django 2.0.5 on 2018-05-13 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_choice_win_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='win_count',
        ),
    ]