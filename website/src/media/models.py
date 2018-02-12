# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from utilities.models import BaseDateTime
from utilities.models import BaseSeo
from globaly.models import GlobalyTags
# Create your models here.

class MediaAlbum(BaseDateTime):

    title = models.CharField(
            _('TITLE_LABEL'),
            max_length=255,
            unique=True,
            blank=True      
        )
    publish = models.BooleanField(
            _('PUBLISH_LABEL'),
            default=True,
        )

    def __unicode__(self):
        return self.title


    def album_title(self):
        return format_html(
                '<span data-id="{1}">{0}</span>',
                self.title, self.id
            )
  
    album_title.allow_tags = True
    class Meta:
        verbose_name = _('MEDIA_ALBUM_TITLE')
        verbose_name_plural = _('MEDIA_ALBUM_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'media_album'
        app_label = 'media'

class MediaImage(BaseDateTime):

    title = models.CharField(
            _('TITLE_LABEL'),
            max_length=255,
            blank=True      
        )
    image = models.TextField(
        _('IMAGE_LABEL'),
       
         blank=True      
        )
    tags = models.ManyToManyField(
            GlobalyTags,
            verbose_name=_('GLOBALY_TAG_TITLE_PLURAL'),
            related_name='media_image_related_tags',

            blank=True
        )
    album = models.ManyToManyField(
            MediaAlbum,
            verbose_name=_('MEDIA_ALBUM_TITLE_PLURAL'),
            related_name='media_image_related_albums',

            blank=True
        )
    rating = models.IntegerField( _('RATTING_LABEL'), default=0)
    content = models.TextField(
            _('CONTENT_LABEL'),
            blank=True
        )
    def __unicode__(self):
        return self.image.name

    def get_albums(self):
        return ",".join([a.title for a in self.album.all()])

    def Tags(self):
        return ",".join([t.name for t in self.tags.all()])

    def thumb(self):
        thumb =  self.get_thumb()
        if thumb is not None:
            return format_html(
                    '<img data-src="{1}" data-title="{2}"  src="data:image/png;base64,{0}" />',
                    thumb, self.image.url, self.title
                )
        else:
            return ""
    thumb.allow_tags = True

    def get_thumb(self):     
        return encode_image_2( self.image, 150, 150)
       

    class Meta:
        verbose_name = _('MEDIA_IMAGE_TITLE')
        verbose_name_plural = _('MEDIA_IMAGE_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'media_image'
        app_label = 'media'
