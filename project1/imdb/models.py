from django.db import models
from embed_video.fields import EmbedVideoField



gender_choices = [('m',"Male"), ('f', 'Female')]
age_rating_choices = [('G', 'General Audiences'), ("PG-13", 'Parents Strongly Cautioned'),
                       ('R', 'Restricted'), ('NC-17', 'Adults Only') ]


class Person(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=gender_choices)
    portrait = models.ImageField(upload_to="persons", blank=True)
    birth_date = models.DateField(blank=True)
    wiki_link = models.URLField(blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    

class Movie(models.Model):
    title = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    poster = models.ImageField(upload_to="posters", blank=True)
    release_date = models.DateField(blank=True)
    duration = models.IntegerField(blank=True)
    age_rating = models.CharField(max_length=5, choices=age_rating_choices)
    wiki_link = models.URLField(blank=True)
    trailer = EmbedVideoField(default="https://www.youtube.com/watch?v=SgmBsEoP1GI")

    def __str__(self):
        return self.title