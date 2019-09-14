import graphene
from django.test import TestCase

from django.test import RequestFactory
from graphene.test import Client
from django_graphql_ratelimit import ratelimit


class MockUser(object):
    def __init__(self, authenticated=False):
        self.pk = 1
        self.is_authenticated = authenticated
        self.META = {"REMOTE_ADDR": "192.168.1.1"}


class RequestSMSCode(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)

    ok = graphene.Boolean()

    # @ratelimit(key="ip", rate="1/m", block=True)
    # @ratelimit(key="user_or_ip", rate="2/m", block=True)
    @ratelimit(key="gql:phone", rate="1/m", block=True)
    def mutate(self, info, phone):
        # request = info.context
        # send sms code logic
        return RequestSMSCode(ok=True)


class Picture(graphene.ObjectType):
    url = graphene.String()


class Query(graphene.ObjectType):
    pictures = graphene.List(Picture)

    @ratelimit(key="user_or_ip", rate="1/m", block=True)
    def resolve_pictures(root, info):
        return [Picture(url="https://o3o3o.me")]


class Mutation(graphene.ObjectType):
    request_sms_code = RequestSMSCode.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


class GqlRatelimitTestCase(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.context = self.rf.get("/")
        self.context.user = MockUser()
        self.client = Client(schema)

    def test_rateliimt_with_gql(self):
        query = """
        mutation {
            requestSmsCode(phone: "+8612345678"){
                ok
            }
        }
        """
        resp = self.client.schema.execute(query, context_value=self.context)
        self.assertIsNone(resp.errors, msg=resp.errors)

        # ratelimited by phone
        resp = self.client.schema.execute(query, context_value=self.context)
        self.assertEqual(str(resp.errors[0]), "rate_limited", msg=resp.errors)

        query = """
        query {
            pictures{
                url
            }
        }
        """
        resp = self.client.schema.execute(query, context_value=self.context)
        self.assertIsNone(resp.errors, msg=resp.errors)

        resp = self.client.schema.execute(query, context_value=self.context)
        # ratelimit by user_or_ip
        self.assertEqual(str(resp.errors[0]), "rate_limited", msg=resp.errors)
