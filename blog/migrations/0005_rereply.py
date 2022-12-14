# Generated by Django 4.1 on 2022-08-24 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_alter_reply_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rereply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_rereplies', to=settings.AUTH_USER_MODEL)),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_rereplay', to='blog.reply')),
            ],
            options={
                'verbose_name_plural': 'Re Replies',
            },
        ),
    ]
