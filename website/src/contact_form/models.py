from django.db import models
from django.utils.translation import ugettext_lazy as _
from utilities.models import BaseDateTime

class Contact(BaseDateTime):
    
    title = models.CharField(
            _('TITLE_LABEL'),
            max_length=255
        )
    name = models.CharField(
            _('NAME_LABEL'),
            max_length=100   
        )
    email = models.EmailField(
            _('EMAIL_LABEL'),
            max_length=255
        )

    body = models.TextField(_('MESSAGE_LABEL'))
    

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('CONTACTS_TITLE')
        verbose_name_plural = _('CONTACTS_TITLE_PLURAL')
        get_latest_by = 'created'
        ordering = ('-id',)
        db_table = 'contact_form_contacts'
        app_label = 'contact_form'
