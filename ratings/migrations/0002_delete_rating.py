# Generated by Django 4.2.2 on 2023-07-01 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rating',
        ),
    ]