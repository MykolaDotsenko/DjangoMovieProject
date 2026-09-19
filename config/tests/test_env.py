import os
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from config.env import env_bool, env_int, env_list, required_env


class EnvironmentParsingTests(SimpleTestCase):
    def test_env_bool_accepts_explicit_true_and_false_values(self):
        for value in ("1", "true", "YES", "on"):
            with self.subTest(value=value), patch.dict(os.environ, {"FLAG": value}):
                self.assertTrue(env_bool("FLAG"))

        for value in ("0", "false", "NO", "off"):
            with self.subTest(value=value), patch.dict(os.environ, {"FLAG": value}):
                self.assertFalse(env_bool("FLAG", True))

    def test_env_bool_uses_default_when_variable_is_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertTrue(env_bool("FLAG", True))
            self.assertFalse(env_bool("FLAG"))

    def test_env_bool_rejects_unknown_values(self):
        with (
            patch.dict(os.environ, {"FLAG": "maybe"}),
            self.assertRaisesMessage(ImproperlyConfigured, "FLAG must be one of"),
        ):
            env_bool("FLAG")

    def test_env_int_parses_values_and_enforces_minimum(self):
        with patch.dict(os.environ, {"PORT": "5433"}):
            self.assertEqual(env_int("PORT", 5432, minimum=1), 5433)

        with (
            patch.dict(os.environ, {"PORT": "0"}),
            self.assertRaisesMessage(ImproperlyConfigured, "PORT must be at least 1"),
        ):
            env_int("PORT", 5432, minimum=1)

    def test_env_int_rejects_non_integer_values(self):
        with (
            patch.dict(os.environ, {"PORT": "five"}),
            self.assertRaisesMessage(ImproperlyConfigured, "PORT must be an integer"),
        ):
            env_int("PORT", 5432)

    def test_env_list_trims_values_and_discards_empty_items(self):
        with patch.dict(os.environ, {"HOSTS": "example.com, ,api.example.com"}):
            self.assertEqual(env_list("HOSTS"), ["example.com", "api.example.com"])

    def test_required_env_rejects_missing_value(self):
        with (
            patch.dict(os.environ, {}, clear=True),
            self.assertRaisesMessage(ImproperlyConfigured, "TOKEN must be set"),
        ):
            required_env("TOKEN")
