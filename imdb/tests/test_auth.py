from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class SignUpViewTests(TestCase):
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

    def test_signup_rejects_duplicate_username(self):
        User.objects.create_user(username="member", password="SafePortfolioPass123!")

        response = self.client.post(
            reverse("imdb:signup"),
            {
                "username": "member",
                "password1": "AnotherSafePass123!",
                "password2": "AnotherSafePass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="member").count(), 1)


class SignInViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="member",
            password="SafePortfolioPass123!",
        )

    def test_login_authenticates_valid_credentials(self):
        response = self.client.post(
            reverse("imdb:login"),
            {
                "username": self.user.username,
                "password": "SafePortfolioPass123!",
            },
        )

        self.assertRedirects(response, reverse("imdb:index"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            reverse("imdb:login"),
            {
                "username": self.user.username,
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)


class SignOutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="member",
            password="SafePortfolioPass123!",
        )
        self.client.force_login(self.user)

    def test_logout_rejects_get(self):
        response = self.client.get(reverse("imdb:logout"))

        self.assertEqual(response.status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout_post_clears_session(self):
        response = self.client.post(reverse("imdb:logout"))

        self.assertRedirects(response, reverse("imdb:index"))
        self.assertNotIn("_auth_user_id", self.client.session)
