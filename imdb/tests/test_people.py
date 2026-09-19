from datetime import date

from django.test import TestCase
from django.urls import reverse

from imdb.models import Movie, Participation, Person


class PersonListViewTests(TestCase):
    def test_people_are_ordered_by_last_name_then_first_name(self):
        Person.objects.create(
            first_name="Zoe",
            last_name="Beta",
            gender=Person.Gender.FEMALE,
        )
        first = Person.objects.create(
            first_name="Amy",
            last_name="Alpha",
            gender=Person.Gender.FEMALE,
        )

        response = self.client.get(reverse("imdb:person-list"))

        self.assertEqual(response.context["people"][0], first)


class PersonDetailViewTests(TestCase):
    def setUp(self):
        self.person = Person.objects.create(
            first_name="Ada",
            last_name="Actor",
            gender=Person.Gender.FEMALE,
        )

    def test_filmography_is_ordered_newest_first(self):
        older = Movie.objects.create(
            title="Older",
            release_date=date(2020, 1, 1),
            age_rating=Movie.AgeRating.GENERAL,
        )
        newer = Movie.objects.create(
            title="Newer",
            release_date=date(2024, 1, 1),
            age_rating=Movie.AgeRating.GENERAL,
        )
        for movie in (older, newer):
            Participation.objects.create(
                movie=movie,
                person=self.person,
                role=Participation.Role.ACTOR,
            )

        response = self.client.get(reverse("imdb:person-detail", args=[self.person.pk]))

        self.assertEqual(
            [credit.movie.title for credit in response.context["credits"]],
            ["Newer", "Older"],
        )

    def test_missing_person_returns_404(self):
        response = self.client.get(reverse("imdb:person-detail", args=[999999]))

        self.assertEqual(response.status_code, 404)
