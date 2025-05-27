from django.urls import resolve, Resolver404


class AppendSlashNoRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        if not path.endswith("/") and not path.startswith("/admin"):
            try:
                resolve(path + "/")
                request.path_info = path + "/"
            except Resolver404:
                pass

        response = self.get_response(request)
        return response
