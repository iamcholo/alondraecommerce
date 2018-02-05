import user as user_site
from django.utils.functional import SimpleLazyObject

def get_user(request):
    
    if not hasattr(request, '_cached_user'):
        request._cached_user = user_site.get_user(request)  
        
    return request._cached_user

class CustomUserAuthMiddleware(object):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user(request))
        
       

