from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        response = JsonResponse({"status": "unhealthy"}, status=503)
    else:
        response = JsonResponse({"status": "ok"})

    response["Cache-Control"] = "no-store"
    return response
