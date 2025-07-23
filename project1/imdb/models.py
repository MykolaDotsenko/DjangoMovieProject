from django.db import models
from embed_video.fields import EmbedVideoField



gender_choices = [('m',"Male"), ('f', 'Female')]
age_rating_choices = [('G', 'General Audiences'), ("PG-13", 'Parents Strongly Cautioned'),
                       ('R', 'Restricted'), ('NC-17', 'Adults Only') ]
role_choices = [('A', 'Actor'), ("D", 'Director'),
                       ('P', 'Producer'), ('C', 'Music Composer') ]


class Person(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=gender_choices)
    portrait = models.ImageField(upload_to="persons")
    birth_date = models.DateField(blank=True)
    wiki_link = models.URLField(blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    

class Movie(models.Model):
    title = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    poster = models.ImageField(upload_to="posters")
    release_date = models.DateField(blank=True)
    duration = models.IntegerField(blank=True)
    age_rating = models.CharField(max_length=5, choices=age_rating_choices)
    wiki_link = models.URLField(blank=True)
    trailer = EmbedVideoField(default="https://www.youtube.com/watch?v=SgmBsEoP1GI")
    genres = models.ManyToManyField("Genre", related_name="movies", blank=True)

    def genres_str(self):
        return " ".join(self.genres.order_by('name').values_list("name", flat=True)) 

    def __str__(self):
        return self.title
    
    def get_actors(self):
        actors = Person.objects.filter(
            participation__movie=self,
            participation__role='A'
        )
        return actors
    
    def get_directors(self):
        directors = Person.objects.filter(
            participation__movie=self,
            participation__role='D'
        )
        return directors

    

class Genre(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Participation(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=role_choices)
    
    def __str__(self):
        return f"{self.person} - {self.movie} ({self.get_role_display()})"