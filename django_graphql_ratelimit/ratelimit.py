import logging
from django.conf import settings
from django.utils.module_loading import import_string
from functools import wraps
from django_ratelimit import ALL, UNSAFE
from django_ratelimit.exceptions import Ratelimited
from django_ratelimit.core import is_ratelimited


logger = logging.getLogger(__name__)

__all__ = ["ratelimit"]


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
                cls = getattr(settings, "RATELIMIT_EXCEPTION_CLASS", Ratelimited)
                raise (import_string(cls) if isinstance(cls, str) else cls)(
                    "rate_limited"
                )
            return fn(root, info, **kw)

        return _wrapped

    return decorator


ratelimit.ALL = ALL
ratelimit.UNSAFE = UNSAFE
