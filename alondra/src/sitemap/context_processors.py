#encoding:utf-8
from django.conf import settings

def get_domain(request):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    return {
        'current_domain': protocol+"://"+request.get_host() ,
    }

