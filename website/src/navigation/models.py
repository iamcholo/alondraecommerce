# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from utilities.models import BaseDateTime
from utilities.models import BasePublish
from utilities.models import BaseSeo
from mptt.managers import TreeManager


class NavigationPosition(BaseDateTime,BasePublish):
    name = models.CharField(
            _('NAME_LABEL'),
            max_length=255,
            unique=True,
            blank=True      
        )

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('NAVIGATION_POSITION_TITLE')
        verbose_name_plural = _('NAVIGATION_POSITION_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'navigation_position'
        app_label = 'navigation'

class ItemManager(TreeManager):
    def get(self, *args, **kwargs):

        if 'item' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['item']))
            kwargs['object_id'] = kwargs['item'].pk
            del(kwargs['item'])
        return super(ItemManager, self).get(*args, **kwargs)

class NavigationItem(MPTTModel, BaseDateTime, BasePublish):
    limit = models.Q(app_label='posts', model='PostCategory') | \
        models.Q(app_label='posts', model='PostItem')
    position = models.ForeignKey(
            NavigationPosition,
            verbose_name=_('NAVIGATION_POSITION_TITLE'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='navigation_item_position_parent'
        )

    parent = TreeForeignKey(
            'self',
            verbose_name=_('PARENT_LABEL'),
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            related_name='navigation_item_parent'
        )

    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=limit,
        verbose_name=_('CONTENT_TYPE_LABEL'),
        null=True,
        blank=True,
    )
    
    object_id = models.PositiveIntegerField(
        verbose_name=_('RELATED_ITEM_LABEL'),
        null=True,
    )
    
    content_object = GenericForeignKey(
            'content_type', 
            'object_id'
        )
    
    view_name = models.TextField(
            _('VIEW_NAME_LABEL'),
            max_length=255,
            null=True,
            blank=True,
        )

    slug = models.CharField(
            _('SLUG_LABEL'),
            unique=True,
            max_length=255,

        )
    objects = ItemManager()



    def __unicode__(self):
        return str(self.id)

    def title(self):
        if hasattr(self.item, 'name'):
            return self.item.name
        if hasattr(self.item, 'title'):
            return self.item.title

    def get_item(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_item(self, item):
        self.content_type = ContentType.objects.get_for_model(type(item))
        self.object_id = item.pk

    item = property(get_item, set_item)
    class Meta:
        verbose_name = _('NAVIGATION_ITEM_LABEL')
        verbose_name_plural = _('NAVIGATION_ITEM_PLURAL_LABEL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'navigation_item'
        app_label = 'navigation'

