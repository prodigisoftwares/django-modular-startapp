# django-modular-startapp

A Django management command that replaces `startapp` with a package-based scaffold — replacing single-file modules like `models.py`, `views.py`, and `tests.py` with proper packages (`models/`, `views/`, `tests/`, etc.).

## Why

Django's built-in `startapp` creates flat single-file modules. As apps grow, splitting `models.py` into `models/` and `views.py` into `views/` becomes necessary anyway. This command starts you off with that structure from the beginning.

## Installation

```bash
pip install django-modular-startapp
```

Add to `INSTALLED_APPS` in your settings:

```python
INSTALLED_APPS = [
    ...
    "django_modular_startapp",
]
```

## Usage

```bash
python manage.py modular_startapp <app_name>
```

To create the app in a specific directory:

```bash
python manage.py modular_startapp <app_name> --directory path/to/dir
```

## Generated Structure

```
<app_name>/
├── __init__.py
├── apps.py
├── urls.py
├── migrations/
│   └── __init__.py
├── admin/
│   └── __init__.py       # stub with admin.site.register example
├── models/
│   └── __init__.py       # stub with import hints
├── views/
│   └── __init__.py       # stub with import hints
└── tests/
    └── __init__.py       # stub with import hints
```

## Notes

- **`models/`** — Add a file per model (e.g. `user.py`) and re-export from `__init__.py` so Django's migration system can discover them.
- **`admin/`** — One file per registered model keeps admin configuration readable.
- **`views/`** — Split by view type or resource (e.g. `list.py`, `detail.py`).
- **`tests/`** — One file per area under test (e.g. `test_models.py`, `test_views.py`).

## Requirements

- Python 3.12+
- Django 4.2+

## License

MIT
