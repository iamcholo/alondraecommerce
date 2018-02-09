# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from utilities.image_base64 import encode_image_3
from utilities.models import BaseDateTime
from utilities.models import BaseArticle
from utilities.models import BaseThumbnailFeatured
from utilities.models import BasePublish
from utilities.models import BaseSeo
from taxes.models import Taxes
from globaly.models import GlobalyTags
from globaly.models import get_meta
from media.models import MediaAlbum
from django.db import connection
from django.utils import timezone
from django.db.models import Count
from django.conf import settings
from django.apps import apps
from user.models import CustomUser as User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from navigation.models import NavigationItem

POST_TYPES_CHOICES = (

    ('post', 'Blog Post'),
    ('page', 'Page'),
    ('game', 'Game'),
    ('game_engine', 'Game Engine'),
    ('video', 'Video'),
    ('forum', 'Forum'),
)


ATTRIBUTES_TYPES_CHOICES = (

    ('choices', 'Choices'),
    ('text', 'Text'),
    ('selectable', 'Selectable'),
    ('date', 'Date'),

)

class PostCategory(MPTTModel, BaseDateTime, BasePublish, BaseSeo):

    parent = TreeForeignKey(
            'self',
            verbose_name=_('PARENT_LABEL'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='post_categories_parent'
        )
    name = models.CharField(
            _('NAME_LABEL'),
            max_length=255,        
            blank=True      
        )
    post_type = models.CharField(
            max_length=20,
            choices=POST_TYPES_CHOICES,
            default="post"
        )
    
    def view_name(self):
        return "category"
    
    view_name = property (view_name)
    
    def is_paginated(self):
        return True
    
    is_paginated = property (is_paginated)
    
    def title_name(self):
        return "%s - %s" % (
            self.get_post_type(), 
            self.name
        )
    
    def get_post_type(self):
        post_types = {
           "post":_('POST_CATEGORY_ARTICLE_TITLE'), 
           'page': _('POST_CATEGORY_PAGE_TITLE'), 
           'video': _('POST_CATEGORY_VIDEO_TITLE')
           }
        return post_types.get(self.post_type)

    @staticmethod
    def get_items_navigation():
        return PostCategory.objects.all().order_by('-post_type')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('CATEGORY_TITLE')
        verbose_name_plural = _('CATEGORY_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'posts_categories'
        app_label = 'posts'

class PostItem(BaseArticle, BaseDateTime, BaseThumbnailFeatured, BaseSeo):

    autor = models.ForeignKey(
            User,
            verbose_name=_('AUTOR_LABEL'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='post_item_autor'
        )

    album = models.ManyToManyField(
            MediaAlbum,
            verbose_name=_('MEDIA_ALBUM_TITLE_PLURAL'),
            related_name='post_item_related_albums',
            blank=True
        )

    categories = models.ManyToManyField(
            PostCategory,
            verbose_name=_('BLOG_CATEGORY_TITLE_PLURAL'),
            related_name='post_item_related_categories',
            blank=True
        )

    tags = models.ManyToManyField(
            GlobalyTags,
            verbose_name=_('GLOBALY_TAG_TITLE_PLURAL'),
            related_name='post_item_related_tags', 
            blank=True
        )

    taxes = models.ManyToManyField(
            Taxes,
            verbose_name=_('TAXES_TITLE_PLURAL'),
            related_name='post_item_related_taxes', 
            blank=True
        )
    
    
    related_posts = models.ManyToManyField(
            'self',
            verbose_name=_('RELATED_ARTICLES_LABEL'),
            related_name='post_item_related_posts',
            blank=True
        )

    publish_date = models.DateTimeField(
            _('Publish Date'), 
            default=timezone.now,
          
        )

    featured_start_date = models.DateTimeField(
            _('Featured Start Date'), 
            null=True, 
            blank=True
        )
    featured_end_date = models.DateTimeField(
            _('Featured End Date'), 
            null=True, 
            blank=True
        )   
    post_type = models.CharField(
            max_length=20,
            choices=POST_TYPES_CHOICES,
            default="post"
        )

    price = models.FloatField(
            _('PRICE_LABEL'),
             default=0.0
        )   
    qty = models.IntegerField(
            _('QTY_LABEL'),
             default=0
        )   


    def __unicode__(self):
        return self.title


    
    def view_name(self):
        return "post_details"

    view_name = property (view_name)
    
    def is_paginated(self):
        if self.post_type == "forum":
            return True
        else:
            return False
    
    is_paginated = property (is_paginated)

    def title_name(self):
        return "%s - %s" % (
            self.get_post_type(), 
            self.title
        )
    
    @staticmethod
    def get_items_navigation():
        return PostItem.objects.all().order_by('-post_type')
    
    def thumb(self):
        thumb =  self.get_thumb()
        if thumb is not None:
            return format_html(
                    '<img src="data:image/png;base64,{0}" />',
                    thumb
                )
        else:
            return "posts"
    thumb.allow_tags = True

    def get_thumb(self):
        thumbnail = self.thumbnail
        if len(thumbnail) > 0:
            
            return encode_image_3(thumbnail)
        return None

    def Tags(self):
        return ",".join([t.name for t in self.tags.all()])

    def Categories(self):
        return ",".join([c.name for c in self.categories.all()])
    
    @staticmethod
    def SitemapToMonth():
        posts = PostItem.objects.filter(publish=True,post_type='post').\
            extra(
                select={
                    'year': "EXTRACT(year FROM created)",
                    'month': "EXTRACT(month FROM created)",
                    'year_month': "EXTRACT(YEAR_MONTH FROM created )"
                }).\
            values('year', 'month', 'year_month').\
            annotate(total=Count('id')).\
            order_by('year_month')
        return posts
    
    @staticmethod
    def SitemapToYear():
        posts = PostItem.objects.filter(publish=True,post_type='post').\
            extra(
                select={
                    'year': "EXTRACT(year FROM created)",
                   
                }).\
            values('year',).\
            annotate(total=Count('id')).\
            order_by('year')
        return posts
    

    @staticmethod
    def SitemapToMonthRawSQl():
        def dictfetchall(cursor):
            "Return all rows from a cursor as a dict"
            desc = cursor.description
            return [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]   
        current_date =  timezone.now()     
        sql = """
                
                SELECT 
                (
                    SELECT created FROM posts_items 
                    where DATE_FORMAT(created, '%Y%m') = DATE_FORMAT(A.created, '%Y%m') 
                    ORDER BY id desc limit 1
                ) as created,
                DATE_FORMAT(A.created, '%Y') as year,
                DATE_FORMAT(A.created, '%m') as month,
                'post-items' as title,
                COUNT(A.id) as total
                FROM posts_items as A
                where A.publish = 1 and A.post_type='post' and (A.publish_date IS NULL or A.publish_date <= NOW()) and A.post_type in ('post','page')
                GROUP BY DATE_FORMAT(A.created, '%Y%m')
            """
        # 
        cursor = connection.cursor()
        cursor.execute(sql)
        data = dictfetchall(cursor)
        cursor.close()
        return data

    @staticmethod
    def SitemapPerYearMonth( year, month):
        return PostItem.objects.filter(publish=True).\
            extra(
                where=[
                    "EXTRACT(year FROM created) = %s ",
                    "EXTRACT(month FROM created) = %s "
                ], 
                params=[year, month]
            )
    
    def get_post_type(self):
        post_types = {
           "post":_('POST_ARTICLE_TITLE'), 
           'page': _('POST_PAGE_TITLE'), 
           'video': _('POST_VIDEO_TITLE')
           }
        return post_types.get(self.post_type)
    class Meta:
        verbose_name = _('POST_ITEM_TITLE')
        verbose_name_plural = _('POST_ITEM_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'posts_items'
        app_label = 'posts'


@receiver(post_save, sender=PostItem)
def updating_post_nav_slug(sender, instance, **kwargs):
    post = instance # 
    try:
        f1 = Q(app_label='posts')
        
        f2 = Q(model='PostItem')
        i = ContentType.objects.get(
            f1 & f2
            )
        i.get_object_for_this_type(id=instance.id)
        cType = ContentType.objects.get_for_model(i)
        parent = NavigationItem.objects.filter(
            object_id=i.id,
            content_type=cType,
            view_name='posts_details'
        ).update(slug=instance.slug)                 
    except ObjectDoesNotExist:
        return None    


@receiver(post_save, sender=PostCategory)
def updating_category_nav_slug(sender, instance, **kwargs):
    post = instance # 
    try:
        f1 = Q(app_label='posts')
        
        f2 = Q(model='PostCategory')
        i = ContentType.objects.get(
            f1 & f2
            )
        i.get_object_for_this_type(id=instance.id)
        cType = ContentType.objects.get_for_model(i)
        parent = NavigationItem.objects.filter(
            object_id=i.id,
            content_type=cType,
            view_name='category'
        ).update(slug=instance.slug)                 
    except ObjectDoesNotExist:
        return None    

class Attributes(BaseDateTime):

    archetype = models.CharField(
            max_length=20,
            choices=ATTRIBUTES_TYPES_CHOICES,
            default="text"
        )
    
    name = models.CharField(
            _('NAME_LABEL'),
            max_length=255,        
            blank=True      
        )


    priceable = models.BooleanField(
            _('PRICEABLE_LABEL'),
            default=True
        )

    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = _('ATTRIBUTES_TITLE')
        verbose_name_plural = _('ATTRIBUTES_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'attributes'
        app_label = 'posts'


class ProductAttributes(BaseDateTime,BaseThumbnailFeatured):

    product = models.ForeignKey(
            PostItem,
            verbose_name=_('PRODUCT_LABEL'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='post_product_attributes_related_product'
        )
    attributes = models.ForeignKey(
            Attributes,
            verbose_name=_('ATTRIBUTES_LABEL'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='post_product_attributes_related_attributes'
        )

    value = models.CharField(
            _('NAME_LABEL'),
            max_length=255,        
            blank=True      
        )

    price = models.FloatField(
            _('NAME_LABEL'),
             blank=True   
        )


    def __unicode__(self):
        return self.value


    class Meta:
        verbose_name = _('PRODUCT_ATTRIBUTES_TITLE')
        verbose_name_plural = _('PRODUCT_ATTRIBUTES_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'posts_product_attributes'
        app_label = 'posts'