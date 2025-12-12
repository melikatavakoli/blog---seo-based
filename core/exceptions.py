from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import (
    NotFound, PermissionDenied, AuthenticationFailed, NotAuthenticated,
    ValidationError, ParseError, MethodNotAllowed, Throttled, NotAcceptable,
    UnsupportedMediaType
)
from rest_framework.response import Response
import logging
from django.conf import settings
import traceback

from config.core.messages import get_error_message
logger = logging.getLogger(__name__)

print("debug",settings.DEBUG)

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')

        if response is None or data is None:
            return super().render({
                'success': False,
                'code': 'no_data',
                'message': 'هیچ داده‌ای موجود نیست.',
                'errors': {}
            }, accepted_media_type, renderer_context)

        if 200 <= response.status_code < 300:
            return super().render(data, accepted_media_type, renderer_context)
        
        return super().render(data, accepted_media_type, renderer_context)

def custom_exception_handler(exc, context):
    if settings.DEBUG:
        return None

    exception_map = {
        NotFound: 'not_found',
        PermissionDenied: 'permission_denied',
        AuthenticationFailed: 'authentication_failed',
        NotAuthenticated: 'not_authenticated',
        ValidationError: 'validation_error',
        ParseError: 'parse_error',
        MethodNotAllowed: 'method_not_allowed',
        Throttled: 'throttled',
        NotAcceptable: 'not_acceptable',
        UnsupportedMediaType: 'unsupported_media_type',
    }

    response = drf_exception_handler(exc, context)

    if response is not None:
        error_key = next((key for exc_type, key in exception_map.items() if isinstance(exc, exc_type)), 'server_error')
        error_info = get_error_message(error_key)
        messages = [{"message": error_info['message']}]

        if isinstance(exc, ValidationError):
            detail = exc.detail
            if isinstance(detail, dict):
                for field, msgs in detail.items():
                    if isinstance(msgs, list):
                        for msg in msgs[:10]:
                            messages.append({"details": f"{field}: {msg}"})
                    else:
                        messages.append({"details": f"{field}: {msgs}"})
            elif isinstance(detail, list):
                for msg in detail:
                    messages.append({"details": str(msg)})
            else:
                messages.append({"details": str(detail)})
        else:
            detail_msg = getattr(exc, 'detail', None)
            if detail_msg and str(detail_msg) != error_info['message']:
                messages.append({"details": str(detail_msg)})

        return Response({
            "error": error_info['code'],
            "status_code": error_info['status'],
            "messages": messages
        }, status=error_info['status'])

    logger.exception("Unhandled exception: %s", exc)
    error_info = get_error_message('server_error')
    return Response({
        "error": error_info['code'],
        "status_code": error_info['status'],
        "messages": [{"message": error_info['message']}]
    }, status=error_info['status'])