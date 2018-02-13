from posts.models import PostCategory
from posts.models import PostItem

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from itertools import chain
from django.template.response import TemplateResponse


def home(request):    
    template_name = 'modules/sitemap/sitemap.xml'
    context = {}
    context['posts'] = PostItem.SitemapToMonthRawSQl()
    context['baseurl'] = request.build_absolute_uri('/')[:-1]

    return TemplateResponse(
            request, 
            template_name, 
            context,
            content_type="text/xml",
        )

def misc(request):    
    template_name = 'modules/sitemap/sitemap-misc.xml'
    context = {}
    context['baseurl'] = request.build_absolute_uri('/')[:-1]
    return  TemplateResponse(
            request, 
            template_name, 
            context,
            content_type="text/xml",
        )


def details(request, slug=None):    
    
    template_name = 'modules/sitemap/post-item.xml'
    context = {}
    year, month = slug.split('-')
    context['posts'] = PostItem.SitemapPerYearMonth(year, month)
    
    context['baseurl'] = request.build_absolute_uri('/')[:-1]
    return TemplateResponse(
            request, 
            template_name, 
            context,
            content_type="text/xml",
        )
