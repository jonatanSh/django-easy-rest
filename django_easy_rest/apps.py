from django.apps import AppConfig
import sys


class ValidateLoading(object):
    dependencies = [
        'rest_framework',
    ]

    def validate_dependencies(self):
        uninstalled = []
        for dependency in self.dependencies:
            try:
                __import__(dependency)
            except ImportError:
                uninstalled += [dependency]
        if uninstalled:
            return ('required dependencies {}, consider installing them by: '
                    'pip').format(','.join(uninstalled))

    def validate(self):
        error = self.validate_dependencies()
        if error:
            print(error)
            sys.exit(-1)


class DjangoEasyRestConfig(AppConfig):
    ValidateLoading().validate()
    name = 'django_easy_rest'
