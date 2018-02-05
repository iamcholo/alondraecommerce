#encoding:utf-8
import os
import json
from django.conf import settings
from django.utils import timezone
from .models import GlobalConfig

def static_site_domain(request):
    context = {
        'time': timezone.now(),
    }
    config = next(iter(GlobalConfig.objects.all()), None)
    if config is not None:
        context['SITE_NAME'] = config.sitename
        context['SITE_DOMAIN'] = config.sitelink
        context['SITE_META_TITLE'] = config.meta_title
        context['SITE_META_DESCRIPTION'] = config.meta_description
    return context

