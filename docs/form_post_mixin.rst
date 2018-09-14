Form post mixin
===============

This mixin is for django generic class based views, it post the django forms using javascript, (no refresh is needed).

.. code-block:: python

    from easy_rest.mixins import FormPostMixin
    from django.views.generic import UpdateView

    class UpdateViewApi(FormPostMixin, UpdateView):
        fields = ['first_name', 'last_name']
        template_name = 'app/test_form_post.html'
        model = User
        success_message = 'model has been changed {}'.format(datetime.now())

        def get_object(self, queryset=None):
            return User.objects.get(pk=1)

.. code-block:: html

    <html lang="en">
        {% load easy_rest %}

        <head>
            {% load_rest_all %}
        </head>
        <body>
            {% include "easy_rest/easy_rest_form.html" with form=form %}
        </body>
    </html>

You can also add an override save function for the form

.. code-block:: python

    from easy_rest.mixins import FormPostMixin
    from django.views.generic import UpdateView

    class UpdateViewApi(FormPostMixin, UpdateView):
        fields = ['first_name', 'last_name']
        template_name = 'app/test_form_post.html'
        model = User
        success_message = 'model has been changed {}'.format(datetime.now())

        def get_object(self, queryset=None):
            return User.objects.get(pk=1)

    @staticmethod
    def form_save_function(form):
        form.save()
        print("form saved")

Requirements
^^^^^^^^^^^^

load all the rest scripts and styles using

.. code-block:: html

    <html>
        {% load easy_rest %}
        <head>
            {% load_rest_all %}
        </head>
    </html>