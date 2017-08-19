
# EASY REST

Easy rest framework is built under django rest framework.

The easy rest adds many useful mixins, and make it very easy to create rest apps

and to integrate rest apps with existing apps

Quick start
-----------
1. install using pip:

```!sh
    pip3 install django-easy-rest
```

2. Add "easy_rest" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'easy_rest',
    ]

3. Include the easy_rest URLconf in your project urls.py like this::

    url(r'^easy_rest/', include('easy_rest.urls')),

4. Configure the url root of easy rest in your project settings.py like this::

    EASY_REST_ROOT_URL = "easy_rest"

# Demo

1. clone this repo

2. install easy rest by

```!sh
    pip3 install django-easy-rest
```

3. head to demo and execute

```!sh
    python3 manage.py migrate
```

4. create your self a superuser by:

```!sh
    python3 manage.py createsuperuser
```

5. that's all now run the server by:

```!sh
    python3 manage.py runserver
```

# easy rest mixins:

1. ApiAbstractionsMixin

2. DecorativeKeysMixin

3. HelpMixin

4. FormPostMixin

5. FunctionUnPackerMixin 

6. ModelUnpacker 

# easy rest views:

1. RestApiView

# easy rest template-tags:

1. {% load_rest_scripts %}

2. {% load_rest_all %}

# more features:

1. auto testing

# example of the rest view:

In this example you are going to learn how to write 

class based view using the rest mixin.

This example also shows the power of the easy rest

# Code:

views.py

```python

from easy_rest import views
from easy_rest.mixins import MethodApiHelpMixin,DecorativeKeysMethodApi

class MethodBased(HelpMixin, DecorativeKeysMixin, FunctionUnPackerMixin, ModelUnpacker, views.RestApiView):
   method_helpers = {'get_username': {"help": {"general": "returns the username of the requested user",
                                                 "general_usage": "suggestting to use the model unpacker mixin"}}}
    def get_username(self, user):
        return {"username": user.username}
```

and that's it

# Preview

input

```json
{"action":"get_username", "with-model": {"field":"auth.User", "query":{"pk":1}}}
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
                "email": "jonatanshimon@gmail.com",
                "id": 1,
                "date_joined": "2017-07-21T19:02:39.414653Z",
                "username": "jonatan",
                "last_name": "",
                "_password": null,
                "password": "pbkdf2_sha256$36000$oqbcQyNRQE2S$QOS41M4rvGlvLZmS4mzlBPA7CftTRuoG3jcQzYL0QvQ="
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
{"action":"get_username", "with-model": [{"field":"auth.User", "query":{"pk":1}, "name":"users"},
{"field":"auth.User", "query":{"pk":2}, "name":"users"}]}
```

this will return a list called users into a function containing two models,
 
a user with a pk of 1 and a user with the pk of 2

2. help and errors

the following input will raise an error because field contains app.model 

```json
{"action":"get_username", "with-model": {"field":"User", "query":{"pk":1}}}
```
easy rest will add the following to the ouput:

```json
    "help": {
        "help-list": "available help entries dict_keys(['general', 'general_usage'])",
        "message": "returns the username of the requested user",
        "general_usage": "specific help use {action:'get_username', help-prefix:'general_usage'}"
    }
```
for a more complex help we can use the following command

```json
{"action":"get_username", "with-model": {"field":"User", "query":{"pk":1}}, "help-prefix":"general_usage"}
```

the output is:

```json
    "help": {
        "help-list": "available help entries dict_keys(['general', 'general_usage'])",
        "message": "suggestting to use the model unpacker mixin",
        "general_usage": "specific help use {action:'get_username', help-prefix:'general_usage'}"
    }
```

# Integrating rest with django GCBV:

The following example is django GCBV update view with a rest post

views.py:

```python

class UpdateViewApi(FormPostMixin, UpdateView):
    fields = ['first_name', 'last_name']
    template_name = 'easy_rest/test.html'
    model = User
    success_message = 'model has been changed {}'.format(datetime.now())

    def get_object(self, queryset=None):
        return User.objects.get(pk=1)

```

template 

```html
{% load easy_rest %}
<html lang="en">
<head>
{% load_rest_all %}
</head>
<body>
{% include "easy_rest/easy_rest_form.html" with form=form %}
</body>
</html>
```

That's it now the easy rest will make the form post rest,

the easy rest also adds success message of post and it places form errors above the form fields.


# Auto testing:

1. the auto test creates a test file based on your api posts

   # **how to use**#
   add the following to your view
```python
    class ApiTest(PostRecordTestGenerator, RestApiView):
        def __init__(self, *args, **kwargs):
            super(ApiTest, self).__init__(*args, **kwargs)
            self.init_test(app_name='demo_app')
```

# **structure** #

this test will generate test.py for your app if not exists already

and will create a file called auto_generated_post_record_test.py

each api post will be recoded and converted into a test,
so you only need to make api posts in order to create your test files

! remember remove the PostRecordTestGenerator mixin upon done

# Mixins:

# **FunctionUnPackerMixin** # 
        
        this mixin is used to unpack json data into python variables
        
        for example unpacking
        
```json
    {"a":"value of a", "b":"value of b"}
```

```python

def test(a, b):
    pass

```

        give a result of a="value of a", b="value of b"
        
        and the python call is
      
```python 
test(a="value of a", b="value of b")
```


# *HelpMixin** # 

        this mixin decorate api errors with a specific or a general error
                
        this mixin can also display specific information about methods in the api
        
        see examples above.
       
# **DecorativeKeysMixin** # 

        this mixin is used to allow api keys translations for example:
        
        without this mixin api calls can be only under the python language convention
        
        example:
       
```json
{"action":"read_book"}
```

        using this mixin the following can be
        
```json
{"action":"read_book"}

{"action":"read book"}

{"action":"read-book"}

{"action":"read:book"}
```
