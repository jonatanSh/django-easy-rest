setup
=====

Installation
^^^^^^^^^^^^
To install the python api package use pip

.. code-block:: bash

    pip install vcore_api


django setup
^^^^^^^^^^^^

add easy rest to your installed apps in settings.py:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'easy_rest',
    ]

for advanced feature the easy rest root should be included in your app urls as follows:

in your urls.py

.. code-block:: python

    url(r'^easy_rest/', include('easy_rest.urls')),

if you change the root url (for instance the url is myproject/api/something) you need to override it in settings.py

.. code-block:: python

    EASY_REST_ROOT_URL = "myproject/api/something"

Base html file
^^^^^^^^^^^^^^

.. code-block:: html

    {% load easy_rest %}
    <head>
        {% load_rest_scripts %}
    </head>