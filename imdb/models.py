from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Person(models.Model):
    class Gender(models.TextChoices):
        MALE = "m", "Male"
        FEMALE = "f", "Female"

    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    portrait = models.ImageField(upload_to="persons", blank=True)
    birth_date = models.DateField(blank=True, null=True)
    wiki_link = models.URLField(blank=True)

    def get_featured_trailer(self):
        return (
            self.credits.exclude(movie__trailer="")
            .order_by("-movie__rating", "movie__title")
            .values_list("movie__trailer", flat=True)
            .first()
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    class AgeRating(models.TextChoices):
        GENERAL = "G", "General Audiences"
        PG_13 = "PG-13", "Parents Strongly Cautioned"
        RESTRICTED = "R", "Restricted"
        ADULTS_ONLY = "NC-17", "Adults Only"

    title = models.CharField(max_length=100)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=Decimal("0.0"),
        validators=[
            MinValueValidator(Decimal("0.0")),
            MaxValueValidator(Decimal("10.0")),
        ],
    )
    poster = models.ImageField(upload_to="posters", blank=True)
    release_date = models.DateField(blank=True, null=True)
    duration = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
    )
    age_rating = models.CharField(max_length=5, choices=AgeRating.choices)
    wiki_link = models.URLField(blank=True)
    trailer = models.URLField(blank=True)
    genres = models.ManyToManyField("Genre", related_name="movies", blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=Decimal("0.0"))
                & models.Q(rating__lte=Decimal("10.0")),
                name="movie_rating_between_0_and_10",
            ),
            models.CheckConstraint(
                condition=models.Q(duration__isnull=True) | models.Q(duration__gt=0),
                name="movie_duration_positive",
            ),
        ]

    def genres_str(self):
        names = (genre.name for genre in self.genres.all())
        return ", ".join(sorted(names, key=str.casefold))

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Participation(models.Model):
    class Role(models.TextChoices):
        ACTOR = "A", "Actor"
        DIRECTOR = "D", "Director"
        PRODUCER = "P", "Producer"
        COMPOSER = "C", "Music Composer"

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="credits",
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="credits",
    )
    role = models.CharField(max_length=1, choices=Role.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("movie", "person", "role"),
                name="unique_movie_person_role",
            ),
        ]

    def __str__(self):
        return f"{self.person} - {self.movie} ({self.get_role_display()})"
