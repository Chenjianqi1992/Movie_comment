# Generated by Django 2.0.7 on 2018-08-07 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_remove_movie_info_movie_published'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie_info',
            old_name='movie_ID',
            new_name='movie_id',
        ),
    ]
