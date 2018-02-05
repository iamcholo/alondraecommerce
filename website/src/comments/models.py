# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from utilities.models import BaseDateTime
from utilities.models import BasePublish
from django.db.models import Count
from django.db.models import Q
from posts.models import PostItem

POST_TYPES_CHOICES = (
    ('post', 'Blog Post'),
    ('page', 'Page'),
    ('video', 'Video'),
    ('forum', 'Forum'),
)

COMMENT_STATUS_CHOICES = (
    ('published', 'Published'),
    ('trashed', 'Trashed'),
    ('blocked', 'Blocked'),
    ('deleted', 'Deleted'),
)

class ItemManager(models.Manager):
    def get(self, *args, **kwargs):

        if 'autor' in kwargs:
            kwargs['autor_content_type'] = ContentType.objects.get_for_model(type(kwargs['autor']))
            kwargs['autor_object_id'] = kwargs['item'].pk
            del(kwargs['autor'])
        return super(ItemManager, self).get(*args, **kwargs)

class Comments(MPTTModel, BaseDateTime, BasePublish):
    limit = models.Q(app_label='user_site', model='UserSite') | \
        models.Q(app_label='auth', model='User') | \
        models.Q(app_label='user', model='CustomUser')
        
    autor_content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=limit,
        verbose_name=_('CONTENT_TYPE_LABEL'),
        null=True,
        blank=True                  
    )
    
    autor_object_id = models.PositiveIntegerField(
        verbose_name=_('RELATED_ITEM_LABEL'),
        null=True,
        blank=True                   
    )
    
    content_object = GenericForeignKey(
            'autor_content_type', 
            'autor_object_id'
        )

    target = models.ForeignKey(
            PostItem,
            verbose_name=_('TARGET_LABEL'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='comments_related_target'
        )

    parent = TreeForeignKey(
            'self',
            verbose_name=_('PARENT_LABEL'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='comments_related_parent'
        )
    comment = models.TextField(
            _('MESSAGE_LABEL'),
            blank=True,
            null=True       
        )
    email = models.CharField(
            max_length=255,
            blank=True,
            null=True    
        )   
    name = models.CharField(
            max_length=20,
            blank=True,
            null=True
        ) 
    website = models.CharField(
            max_length=20,
            blank=True,
            null=True
        )                        
    status = models.CharField(
            max_length=20,
            choices=COMMENT_STATUS_CHOICES,
            default="published"
        )  
    ip = models.CharField(
            max_length=20,
            verbose_name=_('IP_ADDRESS_LABEL'),
            null=True,
            blank=True,
        )      
    post_type = models.CharField(
            max_length=20,
            choices=POST_TYPES_CHOICES,
            default="post"
        )
    objects = ItemManager()
    
    def __unicode__(self):
        return self.comment
   
    def get_autor(self):
        
        if self.autor_object_id is not None:
            return self.autor_content_type.get_object_for_this_type(id=self.autor_object_id)
        else:
            return _('ANONYMUS_LABEL')

    def set_autor(self, item):
        self.autor_content_type = ContentType.objects.get_for_model(type(item))
        self.autor_object_id = item.pk

    autor = property(get_autor, set_autor)

    class Meta:
        verbose_name = _('COMMENTS_TITLE')
        verbose_name_plural = _('COMMENTS_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'comments'
        app_label = 'comments'
