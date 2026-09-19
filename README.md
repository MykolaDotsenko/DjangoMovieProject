# MovieShelf — Django movie catalog

A portfolio-grade Django application for browsing movies, genres, people and credits, with search, authentication and an admin interface.

## What this project demonstrates

- Django 5.2 LTS application structure
- server-rendered responsive UI with Bootstrap
- relational modeling for movies, genres, people and participation roles
- secure Django authentication and password validation
- search and filtering
- media handling with Pillow
- automated tests and GitHub Actions CI
- environment-based settings instead of committed secrets

## Stack

- Python 3.13 / 3.14
- Django 5.2 LTS
- SQLite for local/demo use
- Bootstrap 5
- Pillow
- GitHub Actions
- Ruff

## Project structure

    manage.py
    config/             Django project configuration
    imdb/               main application
    data/demo.sqlite3   optional preloaded demo database
    media_files/        demo media used by the sample database

The old learning-only project that previously lived in project0/ was removed from the active tree during the modernization. Its history remains available in Git.

## Local setup

Create and activate a virtual environment, then install dependencies:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

On Windows PowerShell:

    .venv\Scripts\Activate.ps1

For an empty development database:

    python manage.py migrate

For the preloaded demo data:

    cp data/demo.sqlite3 db.sqlite3
    python manage.py migrate

Run the app:

    python manage.py runserver

Open http://127.0.0.1:8000/

## Environment variables

Production values should be provided through the environment:

- DJANGO_SECRET_KEY
- DJANGO_DEBUG
- DJANGO_ALLOWED_HOSTS
- DJANGO_CSRF_TRUSTED_ORIGINS

The defaults are intentionally development-oriented. Never use the fallback secret key for a real deployment.

## Quality checks

    pip install -r requirements-dev.txt
    ruff check config imdb manage.py
    python manage.py makemigrations --check --dry-run
    python manage.py check
    python manage.py test

The same checks run in CI on Python 3.13 and 3.14.

## Main features

- featured movies ordered by rating
- movie catalog with title/genre search
- movie detail pages with cast, directors and genres
- people directory and filmography
- genre pages
- sign up, sign in and CSRF-protected sign out
- Django admin for catalog management

## Notes

This is a portfolio/demo application. The committed media and data/demo.sqlite3 exist only to make the project easy to evaluate locally. Runtime database files and new media uploads are ignored by Git.
