from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from imdb.models import Genre, Movie, Participation, Person


class MovieModelTests(TestCase):
    def test_optional_date_and_duration_fields_accept_null(self):
        movie = Movie.objects.create(
            title="Unknown Metadata",
            age_rating=Movie.AgeRating.GENERAL,
        )

        self.assertIsNone(movie.release_date)
        self.assertIsNone(movie.duration)

    def test_rating_validation_rejects_out_of_range_values(self):
        for rating in (Decimal("-0.1"), Decimal("10.1")):
            with self.subTest(rating=rating):
                movie = Movie(
                    title="Invalid Rating",
                    rating=rating,
                    age_rating=Movie.AgeRating.GENERAL,
                )
                with self.assertRaises(ValidationError):
                    movie.full_clean()

    def test_database_rejects_out_of_range_rating(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Movie.objects.create(
                title="Invalid Database Rating",
                rating=Decimal("11.0"),
                age_rating=Movie.AgeRating.GENERAL,
            )

    def test_duration_must_be_positive_when_present(self):
        movie = Movie(
            title="Invalid Duration",
            duration=0,
            age_rating=Movie.AgeRating.GENERAL,
        )

        with self.assertRaises(ValidationError):
            movie.full_clean()

    def test_genres_str_is_stable_and_alphabetical(self):
        movie = Movie.objects.create(
            title="Genre Test",
            age_rating=Movie.AgeRating.GENERAL,
        )
        movie.genres.add(
            Genre.objects.create(name="Thriller"),
            Genre.objects.create(name="Drama"),
        )

        self.assertEqual(movie.genres_str(), "Drama, Thriller")


class GenreModelTests(TestCase):
    def test_genre_name_is_unique(self):
        Genre.objects.create(name="Drama")

        with self.assertRaises(IntegrityError), transaction.atomic():
            Genre.objects.create(name="Drama")


class ParticipationModelTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Credits Test",
            age_rating=Movie.AgeRating.PG_13,
        )
        self.person = Person.objects.create(
            first_name="Ada",
            last_name="Actor",
            gender=Person.Gender.FEMALE,
        )

    def test_duplicate_movie_person_role_is_rejected(self):
        Participation.objects.create(
            movie=self.movie,
            person=self.person,
            role=Participation.Role.ACTOR,
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            Participation.objects.create(
                movie=self.movie,
                person=self.person,
                role=Participation.Role.ACTOR,
            )

    def test_same_person_can_have_different_roles_on_same_movie(self):
        Participation.objects.create(
            movie=self.movie,
            person=self.person,
            role=Participation.Role.ACTOR,
        )
        Participation.objects.create(
            movie=self.movie,
            person=self.person,
            role=Participation.Role.PRODUCER,
        )

        self.assertEqual(self.movie.credits.count(), 2)


class PersonModelTests(TestCase):
    def test_featured_trailer_uses_highest_rated_related_movie(self):
        person = Person.objects.create(
            first_name="Grace",
            last_name="Performer",
            gender=Person.Gender.FEMALE,
            birth_date=date(1990, 1, 1),
        )
        lower = Movie.objects.create(
            title="Lower",
            rating=Decimal("7.0"),
            age_rating=Movie.AgeRating.GENERAL,
            trailer="https://example.com/lower",
        )
        higher = Movie.objects.create(
            title="Higher",
            rating=Decimal("9.0"),
            age_rating=Movie.AgeRating.GENERAL,
            trailer="https://example.com/higher",
        )
        for movie in (lower, higher):
            Participation.objects.create(
                movie=movie,
                person=person,
                role=Participation.Role.ACTOR,
            )

        self.assertEqual(person.get_featured_trailer(), "https://example.com/higher")
