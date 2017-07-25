# Django easy rest:

django easy rest is built under django rest framework 

the easy rest does everything as simple as it gets

as you can see in the following examples:

# Examples:

first the easy rest unpackers:

# Easy rest unpackers:

unpacks the data into python variables it features:

1. model unpacking (searching for the right model/s by name and unpack it)

2. variables unpacking

# Example

views.py

```python

from django_easy_rest import views
from django_easy_rest.mixins import MethodApiHelpMixin

class MethodBased(MethodApiHelpMixin, views.ModelMethodBasedApi):
    def get_username(self, user):
        return {"username": user.username}


```

and that's it

input

```json
{"action":"get_username", "get-model": {"field":"auth.User", "query":{"pk":1}}}
```

output (debug mode)

```json

{
    "debug": {
        "processed-data": {
            "user": {
                "_state": {
                    "db": "default",
                    "adding": false
                },
                "first_name": "",
                "is_superuser": true,
                "is_staff": true,
                "last_login": "2017-07-23T11:49:41.804352Z",
                "is_active": true,
                "email": "s@s.com",
                "id": 1,
                "date_joined": "2017-07-21T19:02:39.414653Z",
                "username": "jonatan",
                "last_name": "",
                "_password": null,
                "password": "pbkdf2_sha256$36000$oqbcQyNRQE2S$QOS41M4EvGkvLZpS4mzlBPA7CftTRuoG3jcQzYL0QvQ="
            },
            "action": "get_username"
        }
    },
    "data": {
        "username": "jonatan"
    }
}

```

as we can see the unpacker got the user with a pk of 1

and returned it to the function because the call was made under debug mode the easy-rest

returned a debug field in the data, with useful information about the current query.

# Additional fields:

1. query many users into a users variable
```json
{"action":"get_username", "get-model": [{"field":"auth.User", "query":{"pk":1}, "name":"users"},
{"field":"auth.User", "query":{"pk":2}, "name":"users"}]}
```
this will return a list called users into a function containing two models,
 
a user with a pk of 1 and a user with the pk of 2


# More examples of django easy rest 

# **setup** #

views.py

```python


from django_easy_rest import views
from django_easy_rest.mixins import MethodApiHelpMixin,MethodApiUnPackerMixin


class MethodBased(MethodApiUnPackerMixin,MethodApiHelpMixin,views.MethodBasedApi):
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
from django_easy_rest import views

urlpatterns = [
    url(r'^test/', views.MethodBased.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

```


now we can browse to "localhost:8000/test/"

and check our rest, here are some examples of inputs and outputs

for the following view.

important! note that the outputs add a debug field if settings.DEBUG = True 

# **inputs and outputs** #


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

