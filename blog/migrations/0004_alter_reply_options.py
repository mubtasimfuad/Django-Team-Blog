# Generated by Django 4.1 on 2022-08-23 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_reply'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reply',
            options={'verbose_name_plural': 'Replies'},
        ),
    ]