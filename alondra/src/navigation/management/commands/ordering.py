from django.core.management.base import NoArgsCommand
from django.db import connection
from posts.models import PostItem
from django.db.models import Count
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from navigation.models import NavigationItem
class Command(NoArgsCommand):
    help = 'check youtube videos'

    def handle(self, *args, **options):
	
        print NavigationItem.objects.get(content_object__slug="dadad")
        pass