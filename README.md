# MovieShelf

**A modern Django movie catalog focused on clean backend architecture, secure authentication, relational data modeling, and reliable engineering practices.**

MovieShelf lets users browse movies, genres, cast and directors, search the catalog, explore filmographies, and create accounts through Django's built-in authentication system.

## Highlights

- **Django 5.2 LTS** with a clean `config/` + app structure
- relational modeling for **movies, genres, people, and participation roles**
- search by **movie title or genre**
- movie detail pages with **cast, directors, genres, ratings, trailers, and metadata**
- people directory with **filmography**
- Django-native **sign up, sign in, password validation, and CSRF-protected sign out**
- responsive server-rendered UI with **Bootstrap 5**
- environment-based configuration for secrets, debug mode, hosts, and CSRF origins
- automated tests for core user flows
- **Ruff + Django checks + migration consistency + tests** in GitHub Actions
- CI verified on **Python 3.13 and 3.14**

## Why this project is portfolio-ready

This project was modernized from an earlier learning application into a cleaner, maintainable Django codebase.

The focus is not only on features, but on engineering quality:

- conventional project structure
- framework-native authentication instead of custom password logic
- deterministic and readable ORM queries
- reduced dependency surface
- repository hygiene
- automated validation in CI
- responsive and accessible UI states
- clear local setup and demo data

## Tech stack

| Area | Technology |
| --- | --- |
| Backend | Python, Django 5.2 LTS |
| Database | SQLite for local/demo use |
| Frontend | Django Templates, Bootstrap 5, CSS |
| Media | Pillow |
| Quality | Ruff, Django system checks, automated tests |
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
Django Admin can be used to manage movies, genres, people, participation roles, and profiles.

## Architecture

```text
.
├── config/             # Django project configuration
├── imdb/               # Main application
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── data/
│   └── demo.sqlite3    # Optional preloaded demo database
├── media_files/        # Demo media
├── manage.py
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

The application deliberately keeps the architecture simple: standard Django models, generic/class-based views, built-in authentication, templates, and a small dependency set.

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
pip install -r requirements.txt
```

### 3. Choose a database

Start with an empty database:

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

## Environment variables

For local development, sensible development defaults are provided. For deployment, configure:

```text
DJANGO_SECRET_KEY
DJANGO_DEBUG
DJANGO_ALLOWED_HOSTS
DJANGO_CSRF_TRUSTED_ORIGINS
```

Example values are documented in `.env.example`.

## Quality checks

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the same checks used by CI:

```bash
ruff check config imdb manage.py
python manage.py makemigrations --check --dry-run
python manage.py check
python manage.py test
```

GitHub Actions runs the full quality pipeline on Python 3.13 and 3.14.

## Engineering decisions

### Django-native authentication
Authentication uses Django's built-in forms and auth views rather than duplicating password and session logic.

### Environment-based settings
Secrets and deployment-sensitive values are kept outside source code.

### Small dependency surface
The project avoids unnecessary packages when built-in Django functionality or simple URLs are sufficient.

### Deterministic content selection
Featured content uses explicit ordering rather than expensive random database ordering.

### Repository hygiene
IDE metadata, Python caches, runtime databases, and generated files are excluded from active source control.

## Current scope

MovieShelf is intentionally a focused portfolio application rather than a full commercial IMDb clone.

The next production-oriented extensions would be:

- Docker
- PostgreSQL
- deployment pipeline
- test coverage reporting
- integration/browser tests
- live demo and screenshots

## License

This repository is intended as a personal portfolio and demonstration project.
