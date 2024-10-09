# Generated by Django 5.1.1 on 2024-10-06 18:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_follower'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follower',
            name='is_read',
        ),
        migrations.CreateModel(
            name='FolowerActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_read', models.BooleanField(default=False, null=True)),
                ('follower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='follower_activity', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='following_activity', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'follower_activities',
            },
        ),
    ]
