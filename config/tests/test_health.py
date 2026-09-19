from unittest.mock import patch

from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse


class HealthCheckTests(TestCase):
    def test_health_check_reports_database_readiness(self):
        response = self.client.get(reverse("health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_health_check_rejects_non_get_requests(self):
        response = self.client.post(reverse("health"))

        self.assertEqual(response.status_code, 405)

    @patch("config.views.connection.cursor", side_effect=DatabaseError)
    def test_health_check_returns_503_when_database_is_unavailable(self, cursor):
        response = self.client.get(reverse("health"))

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "unhealthy"})
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        cursor.assert_called_once_with()
