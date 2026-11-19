from django.utils.cache import patch_cache_control


class PrivateNoStoreMiddleware:
    """Evita que el navegador o un proxy guarden en caché páginas con datos de un usuario autenticado
    (por ejemplo, verlas con «atrás» después del logout en un equipo compartido)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if getattr(request, 'user', None) is not None and request.user.is_authenticated:
            patch_cache_control(response, private=True, no_store=True)
        return response
