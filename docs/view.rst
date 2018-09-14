The main rest view
==================

The main view of the api is the RestApiView, with mixins combined this view is very powerful,
there are 3 main optional parameters to initialize:

* function_field_name, default "action", this is the api function in the class see example below

* api_allowed_post_methods, default ["__all__"], this field is for security reasons and defines the avilable methods for post in the class

* api_allowed_get_methods, default ["__all__"], this field is for security reasons and defines the avilable methods for get in the class



Example of the api
^^^^^^^^^^^^^^^^^^

python:

.. code-block:: python

    from easy_rest.views import RestApiView

    class UsersApi(RestApiView):
        api_allowed_post_methods = [
            "authenticate",
        ]

        def authenticate(self, api_data):
            """
            Some authentication code here
            """

            return {
                "data": "user authenticated successfully"
            }


Sync request demo

.. code-block:: javascript

    let api = new RequestHandler("/<url_to_api>/");

    // now lets create a sync post to authenticate a user

    let api_data = api.PostSync({"action": "authenticate"});

    console.log(api_data.data);


Async request demo

.. code-block:: javascript

    let api = new RequestHandler("/<url_to_api>/");

    // now lets create a sync post to authenticate a user

    api.PostASync({"action": "authenticate"}, function(api_data) {
        console.log(api_data.data);
    });

The function field name
^^^^^^^^^^^^^^^^^^^^^^^
this field controls the name of the function field

.. code-block:: javascript

    let api = new RequestHandler("/<url_to_api>/");

    // if function_field_name = "action", the request is
    api.PostSync({"action": "authenticate"});

    // if function_field_name = "something_else", the request is
    api.PostSync({"something_else": "authenticate"});