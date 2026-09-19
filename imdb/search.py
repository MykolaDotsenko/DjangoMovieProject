from django.db import connections
from django.db.models import Exists, OuterRef, Q

from .models import Genre


def search_movies(queryset, query):
    query = query.strip()
    if not query:
        return queryset

    if connections[queryset.db].vendor != "postgresql":
        return queryset.filter(
            Q(title__icontains=query) | Q(genres__name__icontains=query)
        ).distinct()

    return _search_movies_postgresql(queryset, query)


def _search_movies_postgresql(queryset, query):
    from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

    search_query = SearchQuery(query, config="english", search_type="websearch")
    search_vector = SearchVector("title", config="english")
    genre_match = Genre.objects.filter(
        movies=OuterRef("pk"),
        name__icontains=query,
    )

    return (
        queryset.annotate(
            search_vector=search_vector,
            search_rank=SearchRank(search_vector, search_query, cover_density=True),
            genre_match=Exists(genre_match),
        )
        .filter(Q(search_vector=search_query) | Q(title__icontains=query) | Q(genre_match=True))
        .order_by("-search_rank", "-genre_match", "title")
    )
