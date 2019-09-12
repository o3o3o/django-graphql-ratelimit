import graphene
from django.test import TestCase
from django.test import Client, RequestFactory, testcases
from graphene_django.settings import graphene_settings

class SchemaRequestFactory(RequestFactory):
    def __init__(self, **defaults):
        super(SchemaRequestFactory, self).__init__(**defaults)
        self._schema = graphene_settings.SCHEMA

    def schema(self, **kwargs):
        self._schema = graphene.Schema(**kwargs)

    def execute(self, query, **options):
        # options.setdefault('middleware', [JSONWebTokenMiddleware()])
        return self._schema.execute(query, **options)

class GqlRatelimitTestCase(TestCase):
    def test_rateliimt_with_gql(self):
        @ratelimit(key='gql:', rate='1/m')
        def view(request):
