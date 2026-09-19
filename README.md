# MovieShelf

**A modern Django movie catalog focused on clean backend architecture, secure authentication, relational data integrity, and reliable engineering practices.**

MovieShelf lets users browse movies, genres, cast and directors, search the catalog, explore filmographies, and create accounts through Django's built-in authentication system.

## Highlights

- **Django 5.2 LTS** with a clean `config/` + application structure
- relational modeling for **movies, genres, people, and participation roles**
- database-level constraints for ratings, durations, unique genres, and duplicate credits
- search by **movie title or genre**
- movie detail pages with **cast, directors, genres, ratings, trailers, and metadata**
- people directory with **filmography**
- Django-native **sign up, sign in, password validation, and CSRF-protected sign out**
- responsive server-rendered UI with **Bootstrap 5**
- environment-based configuration with fail-fast production settings
- SQLite for zero-friction local/demo use and optional **PostgreSQL-ready configuration**
- database-backed `/health/` readiness endpoint
- console logging with environment-controlled log level
- **27+ automated tests, 99% application coverage, Ruff, migration checks, demo-database migration checks, and deployment checks**
- CI verified on **Python 3.13 and 3.14**

## Why this project is portfolio-ready

MovieShelf was modernized from an earlier learning application into a deliberately small, maintainable Django codebase.

The focus is not on adding layers for their own sake. The project relies on Django's built-in strengths:

- models and database constraints own data integrity
- forms own input validation
- generic/class-based views orchestrate requests and querysets
- templates own presentation
- Django authentication owns password and session behavior
- CI continuously verifies formatting, migrations, tests, coverage, demo-data compatibility, and deployment settings

This keeps the architecture predictable for another Django developer without introducing unnecessary service, repository, or dependency-injection layers.

## Tech stack

| Area | Technology |
| --- | --- |
| Backend | Python, Django 5.2 LTS |
| Database | SQLite locally; PostgreSQL-ready production configuration |
| Frontend | Django Templates, Bootstrap 5, CSS |
| Media | Pillow |
| Quality | Ruff, coverage.py, Django system/deployment checks |
| CI | GitHub Actions |
| Supported Python | 3.13, 3.14 |

## Core features

### Movies
- featured movies ordered by rating
- paginated movie catalog
- search by title and genre
- movie detail pages
- cast and director relationships
- genre navigation
- rating, release year, duration, age rating, trailer, and Wikipedia links

### People
- actors, directors, producers, and composers
- paginated people directory
- individual profile pages
- filmography with participation role
- featured trailer based on related movies

### Accounts
- user registration with Django password validation
- sign in with Django authentication
- authenticated session handling
- CSRF-protected sign out

### Administration
Django Admin manages movies, genres, people, and participation roles.

### Operational readiness
- `GET /health/` checks that the application can reach its configured database
- unhealthy database connections return HTTP `503`
- health responses are marked `Cache-Control: no-store`
- production mode fails fast when required security/database configuration is missing
- logging goes to the console and is controlled with `DJANGO_LOG_LEVEL`

## Architecture

```text
.
├── config/
│   ├── settings.py      # environment, database, logging, security
│   ├── urls.py
│   └── views.py         # infrastructure health check
├── imdb/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_models.py
│   │   ├── test_movies.py
│   │   └── test_people.py
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── data/
│   └── demo.sqlite3
├── media_files/
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── requirements-postgres.txt
└── pyproject.toml
```

The application deliberately keeps one domain app because the current domain is cohesive. Splitting it into multiple apps or adding service/repository layers would add ceremony without improving maintainability at this size.

## Local setup

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Choose a local database

Start with an empty SQLite database:

```bash
python manage.py migrate
```

Or use the included demo data:

```bash
cp data/demo.sqlite3 db.sqlite3
python manage.py migrate
```

### 4. Run the application

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

The health endpoint is available at `http://127.0.0.1:8000/health/`.

## PostgreSQL-ready configuration

SQLite remains the default because it makes the repository easy to clone and evaluate.

For PostgreSQL, install the optional driver:

```bash
python -m pip install -r requirements-postgres.txt
```

Then configure:

```text
DJANGO_DATABASE_BACKEND=postgresql
DJANGO_DB_NAME=movieshelf
DJANGO_DB_USER=movieshelf
DJANGO_DB_PASSWORD=...
DJANGO_DB_HOST=...
DJANGO_DB_PORT=5432
DJANGO_DB_CONN_MAX_AGE=60
```

Django 5.2 supports PostgreSQL 14+ and recommends Psycopg 3.

## Environment variables

The complete example is in `.env.example`.

Important production values include:

```text
DJANGO_SECRET_KEY
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS
DJANGO_CSRF_TRUSTED_ORIGINS
DJANGO_DATABASE_BACKEND
DJANGO_LOG_LEVEL
```

When PostgreSQL is selected, missing database credentials fail fast with a clear configuration error.

## Quality checks

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the same core checks used by CI:

```bash
ruff check .
ruff format --check .
python manage.py makemigrations --check --dry-run
python manage.py check
coverage run manage.py test
coverage report
```

CI additionally:

- migrates the committed demo database to catch real-data migration regressions
- enforces a coverage floor
- runs Django's production `check --deploy --fail-level WARNING`
- validates the project on Python 3.13 and 3.14

## Engineering decisions

### Django-native architecture
The code follows Django's standard MVT model and generic views instead of reproducing framework features behind additional layers.

### Database constraints as invariants
Important rules are enforced by the database as well as application validation, preventing invalid states from being created through code paths outside forms.

### Environment-based settings
Secrets and deployment-sensitive values remain outside source control. Production configuration fails early when critical values are missing.

### SQLite locally, PostgreSQL-ready when needed
SQLite keeps evaluation simple. PostgreSQL support is opt-in so the local developer experience does not gain unnecessary dependencies.

### Small dependency surface
Optional PostgreSQL support lives in a separate requirements file; the default application remains lightweight.

### Operational checks without infrastructure sprawl
A database-aware health endpoint and console logging provide useful deployment primitives without adding Docker, Redis, Celery, or a monitoring framework.

## Portfolio status

The codebase, tests, CI, and deployment configuration are intentionally production-conscious, while the repository remains easy to run locally.

Still intentionally outside this repository:

- hosting-provider-specific deployment configuration
- live demo URL
- real UI screenshots captured from a deployed/running environment
- external monitoring/error-reporting service
- backup infrastructure

Those should be added only when a real deployment target exists rather than simulated in source code.

## License

This repository is intended as a personal portfolio and demonstration project.
