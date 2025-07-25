# Generated by Django 5.2 on 2025-06-15 07:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pl', '0002_programminglanguage_contact_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('portrait', models.ImageField(upload_to='persons')),
                ('birth_date', models.DateField(blank=True)),
                ('wiki_link', models.URLField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='programminglanguage',
            name='creator',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_list', to='pl.person'),
        ),
    ]
