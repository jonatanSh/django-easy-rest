Live context
============

this mixin add a functionality to declare live context section, this section will render automatically live from the server

.. code-block:: python

    from easy_rest.mixins import TemplateContextFetcherMixin
    from django.views import generic

    class ActiveTemplate(TemplateContextFetcherMixin, generic.TemplateView):
        template_name = 'app/live_ctx_demo.html'

        def get_context_data(self, **kwargs):
            return {"time": str(datetime.now()), "random_int": randint(0, 100)}

.. code-block:: html

    <html>
        {% load easy_rest %}
        <head>
            {% load_rest_scripts %}
        </head>
        <body>
            {% livecontext %}
               <h1>Live time from server {time}</h1>

               <h1>Random int from server {random_int}</h1>

            {% endlivecontext %}
        </body>
    </html>

If you want your context from another view (live context tag takes a url)

.. code-block:: html

    <html>
        {% load easy_rest %}
        <head>
            {% load_rest_scripts %}
        </head>
        <body>
            {% livecontext "/url/to/other/template_view" %}
               <h1>Live time from server {time}</h1>

               <h1>Random int from server {random_int}</h1>

            {% endlivecontext %}
        </body>
    </html>
