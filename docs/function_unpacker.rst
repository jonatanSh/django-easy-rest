Function arguments unpacker
===========================

This mixin unpack the request arguments into the function


.. code-block:: python

    from easy_rest.views import RestApiView

    class UsersApi(RestApiView):
        api_allowed_post_methods = [
            "larger_then",
        ]

        def larger_then(self, first_number, second_number):
            return {
                "output": int(first_number) > int(second_number)
            }

.. code-block:: javascript

    let api = new RequestHandler("/api/math");

    api_data = api.PostSync({"action": "larger_then", "first_number": 1, "second_number": 2});

    console.log(api_data.data.output);

The framework will unpack first_number and second_number into the argument field,
the order here doesn't mater it matches the argument strings.