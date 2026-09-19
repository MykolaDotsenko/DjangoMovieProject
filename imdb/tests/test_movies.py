from datetime import date
from decimal import Decimal
from unittest import skipUnless

from django.db import connection
from django.test import TestCase
from django.urls import reverse

from imdb.models import Genre, Movie, Participation, Person


def create_movie(title, *, rating="8.0", release_date=None):
    return Movie.objects.create(
        title=title,
        rating=Decimal(rating),
        release_date=release_date,
        age_rating=Movie.AgeRating.PG_13,
    )


class MovieListViewTests(TestCase):
    def test_search_matches_partial_title(self):
        create_movie("Interstellar")
        create_movie("Unrelated")

        response = self.client.get(reverse("imdb:movie-list"), {"q": "Inter"})

        self.assertContains(response, "Interstellar")
        self.assertNotContains(response, "Unrelated")

    def test_search_matches_genre(self):
        drama = Genre.objects.create(name="Drama")
        match = create_movie("Matching Movie")
        match.genres.add(drama)
        create_movie("Unrelated")

        response = self.client.get(reverse("imdb:movie-list"), {"q": "Drama"})

        self.assertContains(response, "Matching Movie")
        self.assertNotContains(response, "Unrelated")

    def test_empty_search_returns_catalog(self):
        create_movie("Alpha")
        create_movie("Beta")

        response = self.client.get(reverse("imdb:movie-list"), {"q": "  "})

        self.assertEqual(len(response.context["movies"]), 2)

    def test_catalog_is_paginated(self):
        for index in range(13):
            create_movie(f"Movie {index:02d}")

        first_page = self.client.get(reverse("imdb:movie-list"))
        second_page = self.client.get(reverse("imdb:movie-list"), {"page": 2})

        self.assertEqual(len(first_page.context["movies"]), 12)
        self.assertEqual(len(second_page.context["movies"]), 1)

    @skipUnless(connection.vendor == "postgresql", "PostgreSQL-specific full-text search")
    def test_postgresql_search_supports_websearch_operators(self):
        create_movie("Signal Beyond")
        create_movie("Glass Horizon")
        create_movie("Unrelated")

        response = self.client.get(
            reverse("imdb:movie-list"),
            {"q": "Signal OR Horizon"},
        )

        titles = [movie.title for movie in response.context["movies"]]
        self.assertEqual(titles, ["Glass Horizon", "Signal Beyond"])

    @skipUnless(connection.vendor == "postgresql", "PostgreSQL-specific full-text search")
    def test_postgresql_ranks_title_match_before_genre_only_match(self):
        drama = Genre.objects.create(name="Drama")
        direct_match = create_movie("Drama Signal")
        genre_match = create_movie("Quiet Story")
        genre_match.genres.add(drama)

        response = self.client.get(reverse("imdb:movie-list"), {"q": "Drama"})

        movies = list(response.context["movies"])
        self.assertEqual(movies[0], direct_match)
        self.assertIn(genre_match, movies)

    @skipUnless(connection.vendor == "postgresql", "PostgreSQL-specific search indexes")
    def test_postgresql_search_indexes_are_installed(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT indexname
                FROM pg_indexes
                WHERE schemaname = current_schema()
                  AND indexname IN (
                    'movie_title_fts_idx',
                    'movie_title_trgm_idx',
                    'genre_name_trgm_idx'
                  )
                """
            )
            index_names = {row[0] for row in cursor.fetchall()}

        self.assertEqual(
            index_names,
            {
                "movie_title_fts_idx",
                "movie_title_trgm_idx",
                "genre_name_trgm_idx",
            },
        )


class MovieDetailViewTests(TestCase):
    def setUp(self):
        self.movie = create_movie(
            "Detailed Movie",
            rating="8.7",
            release_date=date(2024, 1, 1),
        )
        self.actor = Person.objects.create(
            first_name="Ada",
            last_name="Actor",
            gender=Person.Gender.FEMALE,
        )
        self.director = Person.objects.create(
            first_name="Drew",
            last_name="Director",
            gender=Person.Gender.MALE,
        )
        Participation.objects.create(
            movie=self.movie,
            person=self.actor,
            role=Participation.Role.ACTOR,
        )
        Participation.objects.create(
            movie=self.movie,
            person=self.director,
            role=Participation.Role.DIRECTOR,
        )

    def test_detail_separates_cast_and_directors(self):
        response = self.client.get(reverse("imdb:movie-detail", args=[self.movie.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["actors"]), [self.actor])
        self.assertEqual(list(response.context["directors"]), [self.director])

    def test_missing_movie_returns_404(self):
        response = self.client.get(reverse("imdb:movie-detail", args=[999999]))

        self.assertEqual(response.status_code, 404)


class HomeViewTests(TestCase):
    def test_homepage_uses_highest_rated_movies(self):
        for index in range(7):
            create_movie(f"Movie {index}", rating=str(index))

        response = self.client.get(reverse("imdb:index"))
        titles = [movie.title for movie in response.context["featured_movies"]]

        self.assertEqual(len(titles), 6)
        self.assertNotIn("Movie 0", titles)
        self.assertEqual(titles[0], "Movie 6")


class GenreDetailViewTests(TestCase):
    def test_genre_movies_are_ordered_by_title(self):
        genre = Genre.objects.create(name="Drama")
        second = create_movie("Beta")
        first = create_movie("Alpha")
        genre.movies.add(second, first)

        response = self.client.get(reverse("imdb:genre-detail", args=[genre.pk]))

        self.assertEqual(
            [movie.title for movie in response.context["genre"].movies.all()],
            ["Alpha", "Beta"],
        )
