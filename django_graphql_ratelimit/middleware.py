from ipware import get_client_ip


def ParseClientIpMiddleware(get_response):
    def middleware(request):
        request.META["REMOTE_ADDR"] = get_client_ip(request)[0]
        response = get_response(request)
        return response

    return middleware
