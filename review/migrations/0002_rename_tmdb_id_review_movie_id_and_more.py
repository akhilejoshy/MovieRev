# Generated by Django 5.1.5 on 2025-03-13 22:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='tmdb_id',
            new_name='movie_id',
        ),
        migrations.RenameField(
            model_name='wishlist',
            old_name='tmdb_id',
            new_name='movie_id',
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user', 'movie_id')},
        ),
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together={('user', 'movie_id')},
        ),
    ]
