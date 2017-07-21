# Django easy rest:

django easy rest is built under django rest framework 

the easy rest does everything as simple as it gets

as you can see in the following demo.

in this demo i'll declare 4 rest methods

# Demo 

views.py

```python

from easy_rest import views


class MethodBased(views.MethodApiView):
    method_helpers = {'special_error': {"help": {"general": "this is a special message"}},
                      'super_special': {"help": {"general": "general help",
                                                 "another": "another help"}}}
    api_allowed_methods = ['__all__']

    def correct(self, data):
        return {"test": "test"}

    def error(self, data):
        return 1 / 0

    def special_error(self, data):
        return 1 / 0

    def super_special(self, data):
        return 1 / 0


```

That's it ! 

urls.py

```python
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^test/', views.MethodBased.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

```


now we can browse to "localhost:8000/test/"

and check our rest, here are some examples of inputs and outputs

for the following view.

important! note that the outputs add a debug field if settings.DEBUG = True 

input:

```json
{"action":"correct"}
```

output:

```json
{
    "test": "test"
}
```

input:

```json
{"action":"error"}
```

output:

```json
{
    "debug": {
        "exception-args": [
            "division by zero"
        ],
        "exception-type": "<class 'ZeroDivisionError'>"
    },
    "action": "error",
    "error": "Exception occurred in method check function usage"
}
```

input:

```json
{"action":"special_error"}
```

output:

```json
{
    "debug": {
        "exception-args": [
            "division by zero"
        ],
        "exception-type": "<class 'ZeroDivisionError'>"
    },
    "help": {
        "help-list": "available help entries dict_keys(['general'])",
        "message": "this is a special message",
        "usage": "specific help use {action:special_error, help-prefix:specific error}"
    }
}
```



input:

```json
{"action":"super_special", "help-prefix":"another"}
```

output:

```json
{
    "debug": {
        "exception-args": [
            "division by zero"
        ],
        "exception-type": "<class 'ZeroDivisionError'>"
    },
    "help": {
        "help-list": "available help entries dict_keys(['general', 'another'])",
        "message": "another help",
        "usage": "specific help use {action:super_special, help-prefix:specific error}"
    }
}
```

