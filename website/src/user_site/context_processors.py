def user_site(request):

    if hasattr(request, 'user_site'):
        user = request.user_site
    else:
        from django.contrib.auth.models import AnonymousUser        
        user = AnonymousUser()
    return {
        "user_site": user
    }