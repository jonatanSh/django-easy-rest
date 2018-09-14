Model unpacker mixin
====================

Unpacks the request model into the handling function


.. code-block:: python

    from easy_rest.views import RestApiView

    class UsersApi(RestApiView):
        api_allowed_get_methods = [
            "get_username",
        ]

        def user_name(self, user):
            return {
                "user_name": user.username
            }

.. code-block:: javascript

    let api = new RequestHandler("/api/math");

    api_data = api.PostSync({"action":"get_username", "with-model": {"field":"auth.User", "query":{"pk":1}}});

    console.log(api_data.data.user_name);

Security
^^^^^^^^
Keep security in mind when using this feature.