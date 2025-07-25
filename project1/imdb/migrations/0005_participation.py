# Generated by Django 5.2 on 2025-07-17 14:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imdb', '0004_genre_movie_genres'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('A', 'Actor'), ('D', 'Director'), ('P', 'Producer'), ('C', 'Music Composer')], max_length=1)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imdb.movie')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imdb.person')),
            ],
        ),
    ]
