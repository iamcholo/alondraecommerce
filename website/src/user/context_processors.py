def user(request):

    if hasattr(request, 'user'):
        user = request.user
        
    else:
        from django.contrib.auth.models import AnonymousUser        
        user = AnonymousUser()
    return {
        "user": user
    }