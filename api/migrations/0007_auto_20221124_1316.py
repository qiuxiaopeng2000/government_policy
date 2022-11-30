# Generated by Django 3.2.5 on 2022-11-24 05:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0006_follow_follow_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_info_data',
            name='password',
        ),
        migrations.RemoveField(
            model_name='user_info_data',
            name='username',
        ),
        migrations.AddField(
            model_name='user_info_data',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]