# Generated by Django 4.1.5 on 2023-07-10 09:45

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0004_alter_feedback_managers_alter_userprogress_managers_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='feedback',
            managers=[
                ('Objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='userprogress',
            managers=[
                ('Objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
