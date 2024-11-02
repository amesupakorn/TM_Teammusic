# Generated by Django 5.1.1 on 2024-11-02 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_alter_song_s3_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='s3_alblumurl',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
        migrations.AlterField(
            model_name='singer',
            name='s3_photourl',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
    ]