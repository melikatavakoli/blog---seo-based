import threading

_user_local = threading.local()

def get_current_user_id():
    return getattr(_user_local, "user_id", None)

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            _user_local.user_id = str(user.id)
        else:
            _user_local.user_id = None

        response = self.get_response(request)
        return response
