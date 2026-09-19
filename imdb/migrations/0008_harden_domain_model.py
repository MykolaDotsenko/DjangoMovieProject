from decimal import Decimal

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("imdb", "0007_alter_movie_poster_alter_person_portrait"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Profile",
        ),
        migrations.AlterField(
            model_name="person",
            name="birth_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="rating",
            field=models.DecimalField(
                decimal_places=1,
                default=Decimal("0.0"),
                max_digits=3,
                validators=[
                    django.core.validators.MinValueValidator(Decimal("0.0")),
                    django.core.validators.MaxValueValidator(Decimal("10.0")),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="release_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="duration",
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="trailer",
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name="genre",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="participation",
            name="movie",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="credits",
                to="imdb.movie",
            ),
        ),
        migrations.AlterField(
            model_name="participation",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="credits",
                to="imdb.person",
            ),
        ),
        migrations.AddConstraint(
            model_name="movie",
            constraint=models.CheckConstraint(
                condition=models.Q(rating__gte=Decimal("0.0"))
                & models.Q(rating__lte=Decimal("10.0")),
                name="movie_rating_between_0_and_10",
            ),
        ),
        migrations.AddConstraint(
            model_name="movie",
            constraint=models.CheckConstraint(
                condition=models.Q(duration__isnull=True) | models.Q(duration__gt=0),
                name="movie_duration_positive",
            ),
        ),
        migrations.AddConstraint(
            model_name="participation",
            constraint=models.UniqueConstraint(
                fields=("movie", "person", "role"),
                name="unique_movie_person_role",
            ),
        ),
    ]
