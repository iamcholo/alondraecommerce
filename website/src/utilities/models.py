from django.db import models
from django.utils.translation import ugettext_lazy as _

class BaseDateTime(models.Model):

    created = models.DateTimeField(_('CREATED_LABEL'), auto_now_add=True)
    modified = models.DateTimeField(_('MODIFIED_LABEL'), auto_now=True)

    class Meta:
        abstract = True

class BaseSeo(models.Model):
    slug = models.CharField(
            _('SLUG_LABEL'),
            unique=True,
            max_length=255,

        )
    meta_title = models.CharField(
            _('META_TITLE_LABEL'),
            max_length=255,
 
        )
    meta_description = models.CharField(
            _('META_DESCRIPTION_LABEL'),
            max_length=156,
            blank=True
        )

    class Meta:
        abstract = True

class BasePublish(models.Model):

    publish = models.BooleanField(
            _('PUBLISH_LABEL'),
            default=True,
        )
    class Meta:
        abstract = True

class BaseContent(BasePublish):
    
    title = models.CharField(
            _('TITLE_LABEL'),
            max_length=255,
            
            blank=True      
        )

    excerpt = models.TextField(
            _('EXCERPT_LABEL'),
            blank=True
        )
    content = models.TextField(
            _('CONTENT_LABEL'),
            blank=True
        )

    class Meta:
        abstract = True

class BaseArticle(BaseContent):

    is_featured = models.BooleanField(
            _('IS_FEATURED_LABEL'),
            default=True,
        )


    is_on_feed = models.BooleanField(
            _('IS_ON_FEED_LABEL'),
            default=True,
        )


    class Meta:
        abstract = True

class BaseThumbnailFeatured(models.Model):


    thumbnail = models.TextField(
            _('THUNBNAIL_LABEL'),
            blank=True, 
            null=True
        )
    thumbnail_text = models.CharField(
            _('ATL_TEXT_LABEL'), 
            max_length=255,
            null=True, 
            blank=True
        )
    featured_image = models.TextField(
            _('FEATURED_IMAGE_LABEL'),
            blank=True, 
            null=True
        )
    featured_image_text = models.CharField(
            _('ATL_TEXT_LABEL'), 
            max_length=255,
            null=True, 
            blank=True
        )

    class Meta:
        abstract = True

