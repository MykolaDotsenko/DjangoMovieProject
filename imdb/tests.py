from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Genre, Movie, Participation, Person

User = get_user_model()


class MovieShelfTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Drama")
        self.movie = Movie.objects.create(
            title="Test Movie",
            rating=8.7,
            poster="posters/test.jpg",
            release_date=date(2024, 1, 1),
            duration=120,
            age_rating="PG-13",
            wiki_link="https://example.com/movie",
            trailer="https://www.youtube.com/watch?v=example",
        )
        self.movie.genres.add(self.genre)
        self.person = Person.objects.create(
            first_name="Ada",
            last_name="Actor",
            gender="f",
            portrait="persons/test.jpg",
            birth_date=date(1990, 1, 1),
            wiki_link="https://example.com/person",
        )
        Participation.objects.create(movie=self.movie, person=self.person, role="A")

    def test_homepage_renders_featured_content(self):
        response = self.client.get(reverse("imdb:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Movie")
        self.assertContains(response, "Ada Actor")

    def test_movie_search_matches_title(self):
        response = self.client.get(reverse("imdb:movie-list"), {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Movie")

    def test_movie_search_matches_genre(self):
        response = self.client.get(reverse("imdb:movie-list"), {"q": "Drama"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Movie")

    def test_movie_detail_exposes_actor(self):
        response = self.client.get(reverse("imdb:movie-detail", args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ada Actor")

    def test_signup_creates_and_authenticates_user(self):
        response = self.client.post(
            reverse("imdb:signup"),
            {
                "username": "newuser",
                "password1": "SafePortfolioPass123!",
                "password2": "SafePortfolioPass123!",
            },
        )
        self.assertRedirects(response, reverse("imdb:index"))
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_signup_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("imdb:signup"),
            {
                "username": "broken",
                "password1": "SafePortfolioPass123!",
                "password2": "DifferentPortfolioPass123!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="broken").exists())

    def test_logout_requires_post_and_clears_session(self):
        user = User.objects.create_user(username="member", password="SafePortfolioPass123!")
        self.client.force_login(user)
        response = self.client.post(reverse("imdb:logout"))
        self.assertRedirects(response, reverse("imdb:index"))
        self.assertNotIn("_auth_user_id", self.client.session)
