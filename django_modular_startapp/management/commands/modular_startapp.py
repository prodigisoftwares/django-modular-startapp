import os
from django.core.management.base import BaseCommand, CommandError

PACKAGE_DIRS = ["models", "views", "admin", "tests"]

APPS_PY = """\
from django.apps import AppConfig


class {class_name}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{app_name}"
"""

URLS_PY = """\
from django.urls import path

app_name = "{app_name}"

urlpatterns = []
"""

INIT_MODELS = """\
# Import your models here so Django can discover them.
# Example:
# from .my_model import MyModel
"""

INIT_VIEWS = """\
# Import your views here.
# Example:
# from .my_view import MyView
"""

INIT_ADMIN = """\
# Register your models with the admin here.
# Example:
# from django.contrib import admin
# from {app_name}.models import MyModel
# admin.site.register(MyModel)
"""

INIT_TESTS = """\
# Import your test cases here.
# Example:
# from .test_models import MyModelTests
"""

MIGRATIONS_INIT = """\
"""


class Command(BaseCommand):
    help = "Creates a new Django app with package-based module structure"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str, help="Name of the app to create")
        parser.add_argument(
            "--directory",
            "-d",
            type=str,
            default=None,
            help="Optional path to create the app in (defaults to current directory)",
        )

    def handle(self, *args, **options):
        app_name = options["app_name"]
        base_dir = options["directory"] or os.getcwd()
        app_dir = os.path.join(base_dir, app_name)

        if os.path.exists(app_dir):
            raise CommandError(f"Directory '{app_dir}' already exists.")

        class_name = app_name.replace("_", " ").title().replace(" ", "")

        # Create root app dir
        os.makedirs(app_dir)

        # apps.py
        self._write(
            app_dir, "apps.py", APPS_PY.format(class_name=class_name, app_name=app_name)
        )

        # __init__.py
        self._write(app_dir, "__init__.py", "")

        # urls.py
        self._write(app_dir, "urls.py", URLS_PY.format(app_name=app_name))

        # migrations/
        migrations_dir = os.path.join(app_dir, "migrations")
        os.makedirs(migrations_dir)
        self._write(migrations_dir, "__init__.py", MIGRATIONS_INIT)

        # Package directories
        init_content = {
            "models": INIT_MODELS,
            "views": INIT_VIEWS,
            "admin": INIT_ADMIN.format(app_name=app_name),
            "tests": INIT_TESTS,
        }

        for pkg in PACKAGE_DIRS:
            pkg_dir = os.path.join(app_dir, pkg)
            os.makedirs(pkg_dir)
            self._write(pkg_dir, "__init__.py", init_content[pkg])

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created modular app '{app_name}' at {app_dir}"
            )
        )

    def _write(self, directory, filename, content):
        path = os.path.join(directory, filename)
        with open(path, "w") as f:
            f.write(content)
