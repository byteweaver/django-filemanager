#!/usr/bin/env python
import sys

from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=(
            'filemanager',
        ),
        SECRET_KEY='testing-with-very-secure-key',
        TEST_RUNNER='django_coverage.coverage_runner.CoverageRunner',
    )


from django.test.utils import get_runner


TestRunner = get_runner(settings)


def runtests():
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['filemanager', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
