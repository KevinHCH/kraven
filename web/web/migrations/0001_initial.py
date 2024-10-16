# Generated by Django 5.1.1 on 2024-10-16 21:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, null=True)),
                ('posted_at', models.CharField(max_length=100)),
                ('job_type', models.CharField(max_length=100)),
                ('experience_level', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('posted_at_datetime', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('price', models.TextField(blank=True, null=True)),
                ('sended_at', models.DateTimeField(blank=True, null=True)),
                ('topic_name', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'jobs',
                'managed': False,
            },
        ),
    ]
