[![CircleCI](https://circleci.com/gh/o3o3o/django-graphql-ratelimit.svg?style=svg)](https://circleci.com/gh/o3o3o/django-graphql-ratelimit) [![PyPI version](https://badge.fury.io/py/django-graphql-ratelimit.svg)](https://badge.fury.io/py/django-graphql-ratelimit)

Eaiser to use [django-ratelimit](https://github.com/jsocol/django-ratelimit) for graphql in django.


# Install

```
pip install django-graphql-ratelimit
```

# Usage

ratelimit key support `gql:xxx`, where `xxx` is argument.

```python
from django_graphql_ratelimit import ratelimit

class RequestSMSCode(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)

    ok = graphene.Boolean()

    @ratelimit(key="ip", rate="10/m", block=True)
    @ratelimit(key="gql:phone", rate="5/m", block=True)
    def mutate(self, info, phone):
        request = info.context
        # send sms code logic
        return RequestSMSCode(ok=True)
```
You can use [django-ratelimit keys](https://django-ratelimit.readthedocs.io/en/latest/keys.html#common-keys) except `get:xxx` and `post:xxx`:
* `ip`  - Use the request IP address (i.e. `request.META['REMOTE_ADDR']`)
I suggest you to use [django-ipware](https://github.com/un33k/django-ipware) to get client ip, modify your `MIDDLEWARE` in settings: 
```
MIDDLEWARE = [
"django_graphql_ratelimit.middleware.ParseClientIpMiddleware",
...
]
```

* `header:x-x`   - Use the value of request.META.get('HTTP_X_X', '').
* `user`  - Use an appropriate value from request.user. Do not use with unauthenticated users.
* `user_or_ip`   - Use an appropriate value from `request.user` if the user is authenticated, otherwise use `request.META['REMOTE_ADDR']`.
