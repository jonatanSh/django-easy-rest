Automated testing
=================

In rest api the functionality we often need to test is the request and response,
the framework contains an automated test mixin

Generate a test
^^^^^^^^^^^^^^^

just add the PostRecordTestGenerator to your view and in the init function init the test

.. code-block:: python

    from easy_rest.test_framework.recorder.post_record_mixins import PostRecordTestGenerator
    class ApiTest(PostRecordTestGenerator, RestApiView):

        def __init__(self, *args, **kwargs):
            super(ApiTest, self).__init__(*args, **kwargs)
            self.init_test(app_name='demo_app')

        def echo(self, data):
            return {"echo": data}

then run some requests for example:

.. code-block:: javascript

    let api = new RequestHandler("/some_url");

    api.PostSync({});
    api.PostSync({"action":"echo", "data":"hello"});


The framework will generate tests for you

Generated test example
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from django.test import TestCase
    from demo_app.views import ApiTest
    from django.test import RequestFactory
    from django.contrib.auth.models import AnonymousUser, User
    from easy_rest.test_framework.resolvers.resolve import register_unittest
    from django.test.utils import override_settings

    register_unittest()


    def resolve_user(pk):
        try:
            return User.objects.get(pk=pk)
        except Exception:
            return AnonymousUser()


    class TestApiTest(TestCase):
        @override_settings(DEBUG=True)
        def test_echo(self):
            request = RequestFactory()
            request.data = {'action': 'echo', 'data': 'asdf'}
            request.user = resolve_user(None)
            result = {'debug': {'api-attributes': {'api-allowed-methods': ['__all__']},
                                'processed-data': {'action': 'echo', 'data': 'asdf'}},
                      'debug-mode': ['enabled', 'to disable go to settings.py and change DEBUG=True to false'],
                      'data': {'echo': 'asdf'}}
            if type(result) is dict:
                return self.assertDictEqual(result, self.test.post(request).data)
            return self.assertEqual(result, self.test.post(request).data)

        def __init__(self, *args, **kwargs):
            super(TestApiTest, self).__init__(*args, **kwargs)
            self.test = ApiTest()

        @override_settings(DEBUG=True)
        def test_easy_rest_2017_08_26_12_38_31_143966_test(self):
            request = RequestFactory()
            request.data = {}
            request.user = resolve_user(None)
            result = {'error': 'no action in data',
                      'debug': {'api-attributes': {'api-allowed-methods': ['__all__']}, 'processed-data': {}},
                      'debug-mode': ['enabled', 'to disable go to settings.py and change DEBUG=True to false']}
            if type(result) is dict:
                return self.assertDictEqual(result, self.test.post(request).data)
            return self.assertEqual(result, self.test.post(request).data)