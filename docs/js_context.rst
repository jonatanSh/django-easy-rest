Javascript context
==================

This mixin allows you to access the view context using javascript


.. code-block:: python

    from easy_rest.mixins import TemplateContextFetcherMixin
    from django.views import generic

    class ActiveTemplate(JavascriptContextMixin, generic.TemplateView):
        template_name = 'demo_app/home.html'


        def get_context_data(self, **kwargs):
            ctx = super(WelcomePage, self).get_context_data(**kwargs)
            ctx['message'] = "This is javascript context mixin"
            return ctx


.. code-block:: javascript

    let consts = window.restConsts;

    // now to access the context, do the following:
    console.log(consts.context);
    console.log(consts.context.message);


Requirements
^^^^^^^^^^^^

Requirements for the javascript context

.. code-block:: html

    <html>
        {% load easy_rest %}
        <head>
            {% load_rest_scripts %}
        </head>
    </html>
