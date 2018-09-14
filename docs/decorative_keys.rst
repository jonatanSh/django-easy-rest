Decorative keys mixin
=====================

This mixin is really simple, it make your function_field_name value everything decorative,
if the function name is authenticate_user then the request will look like:

.. code-block:: javascript

    let api = new RequestHandler("/<url_to_api>/");

    api.PostSync({"action": "authenticate_user"});

With decorative keys the request can be:

.. code-block:: javascript

    let api = new RequestHandler("/<url_to_api>/");

    api.PostSync({"action": "authenticate_user"});
    api.PostSync({"action": "authenticate user"});
    api.PostSync({"action": "authenticate-user"});
    api.PostSync({"action": "authenticate:user"});
