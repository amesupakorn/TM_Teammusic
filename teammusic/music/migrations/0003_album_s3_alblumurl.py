# Generated by Django 5.1.1 on 2024-11-02 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_singer_s3_photourl'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='s3_alblumurl',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]