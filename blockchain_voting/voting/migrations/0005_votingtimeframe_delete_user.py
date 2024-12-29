# Generated by Django 5.1.4 on 2024-12-29 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_user_groups_user_is_active_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VotingTimeframe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
