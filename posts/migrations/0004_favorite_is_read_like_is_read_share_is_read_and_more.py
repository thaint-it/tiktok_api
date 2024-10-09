# Generated by Django 5.1.1 on 2024-10-06 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_message_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='is_read',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='like',
            name='is_read',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='share',
            name='is_read',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='view',
            name='is_read',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
