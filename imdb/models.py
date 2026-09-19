from django.contrib.auth.models import User
from django.db import models

GENDER_CHOICES = [("m", "Male"), ("f", "Female")]
AGE_RATING_CHOICES = [
    ("G", "General Audiences"),
    ("PG-13", "Parents Strongly Cautioned"),
    ("R", "Restricted"),
    ("NC-17", "Adults Only"),
]
ROLE_CHOICES = [
    ("A", "Actor"),
    ("D", "Director"),
    ("P", "Producer"),
    ("C", "Music Composer"),
]


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars", blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


class Person(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    portrait = models.ImageField(upload_to="persons", blank=True)
    birth_date = models.DateField(blank=True)
    wiki_link = models.URLField(blank=True)

    def get_featured_trailer(self):
        return (
            Movie.objects.filter(participation__person=self)
            .exclude(trailer="")
            .order_by("-rating", "title")
            .values_list("trailer", flat=True)
            .first()
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    poster = models.ImageField(upload_to="posters", blank=True)
    release_date = models.DateField(blank=True)
    duration = models.IntegerField(blank=True)
    age_rating = models.CharField(max_length=5, choices=AGE_RATING_CHOICES)
    wiki_link = models.URLField(blank=True)
    trailer = models.URLField(
        blank=True,
        default="https://www.youtube.com/watch?v=SgmBsEoP1GI",
    )
    genres = models.ManyToManyField("Genre", related_name="movies", blank=True)

    def genres_str(self):
        return ", ".join(self.genres.order_by("name").values_list("name", flat=True))

    def get_actors(self):
        return (
            Person.objects.filter(participation__movie=self, participation__role="A")
            .distinct()
            .order_by("last_name", "first_name")
        )

    def get_directors(self):
        return (
            Person.objects.filter(participation__movie=self, participation__role="D")
            .distinct()
            .order_by("last_name", "first_name")
        )

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Participation(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.person} - {self.movie} ({self.get_role_display()})"
