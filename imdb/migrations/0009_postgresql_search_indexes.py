from django.db import migrations


SEARCH_INDEXES = (
    "movie_title_fts_idx",
    "movie_title_trgm_idx",
    "genre_name_trgm_idx",
)


def create_postgresql_search_indexes(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return

    schema_editor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    schema_editor.execute(
        """
        CREATE INDEX IF NOT EXISTS movie_title_fts_idx
        ON imdb_movie
        USING GIN (
            to_tsvector(
                'english'::regconfig,
                COALESCE(title, ''::character varying)
            )
        )
        """
    )
    schema_editor.execute(
        """
        CREATE INDEX IF NOT EXISTS movie_title_trgm_idx
        ON imdb_movie
        USING GIN (title gin_trgm_ops)
        """
    )
    schema_editor.execute(
        """
        CREATE INDEX IF NOT EXISTS genre_name_trgm_idx
        ON imdb_genre
        USING GIN (name gin_trgm_ops)
        """
    )


def drop_postgresql_search_indexes(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return

    for index_name in SEARCH_INDEXES:
        schema_editor.execute(f'DROP INDEX IF EXISTS "{index_name}"')


class Migration(migrations.Migration):
    dependencies = [
        ("imdb", "0008_harden_domain_model"),
    ]

    operations = [
        migrations.RunPython(
            create_postgresql_search_indexes,
            drop_postgresql_search_indexes,
        ),
    ]
