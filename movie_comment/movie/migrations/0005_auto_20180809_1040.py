# Generated by Django 2.0.7 on 2018-08-09 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_auto_20180808_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie_info',
            name='movie_update',
            field=models.DateTimeField(null=True, verbose_name='movie updatetime'),
        ),
        migrations.AlterField(
            model_name='movie_comments',
            name='movie_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movie_info'),
        ),
    ]
