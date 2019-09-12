import logging
from ratelimit import ALL
from functools import wraps
from ratelimit.exceptions import Ratelimited
from ratelimit.utils import is_ratelimited

logger = logging.getLogger(__name__)


def GQLRatelimitKey(group, request):
    return request.gql_rl_field


def ratelimit(group=None, key=None, rate=None, method=ALL, block=False):
    def decorator(fn):
        @wraps(fn)
        def _wrapped(root, info, **kw):
            request = info.context

            old_limited = getattr(request, "limited", False)

            if key and key.startswith("gql:"):
                _key = key.split("gql:")[1]
                value = kw.get(_key, None)
                if not value:
                    raise ValueError(f"Cannot get key: {key}")
                request.gql_rl_field = value

                new_key = GQLRatelimitKey
            else:
                new_key = key

            ratelimited = is_ratelimited(
                request=request,
                group=group,
                fn=fn,
                key=new_key,
                rate=rate,
                method=method,
                increment=True,
            )

            request.limited = ratelimited or old_limited

            if ratelimited and block:
                # logger.warn(
                #    "url:<%s> is denied for <%s> in Ratelimit"
                #    % (request.path, request.META["REMOTE_ADDR"])
                # )
                raise Ratelimited("rate_limited")
            return fn(root, info, **kw)

        return _wrapped

    return decorator
