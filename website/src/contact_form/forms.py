from django import forms
from django.conf import settings
from django.template import loader
from django.template import RequestContext
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from utils.send_email import send_mail
from contact_form.models import Contact

class ContactForm(forms.Form):
  
    def __init__(self, data=None, files=None, request=None, *args, **kwargs):
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")
        super(ContactForm, self).__init__(data=data, files=files, *args, **kwargs)
        self.request = request

    title = forms.CharField(max_length=255,
                           label=_('TITLE_LABEL'))    
    name = forms.CharField(max_length=255,
                           label=  _('NAME_LABEL'))
    email = forms.EmailField(max_length=255,
                             label=_('EMAIL_LABEL'))
    body = forms.CharField(widget=forms.Textarea,
                              label=_('MESSAGE_LABEL'))
    
    from_email = settings.DEFAULT_FROM_EMAIL
    
    recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]

    template_name = 'contact_form'
  
    def save(self, fail_silently=False):

        data = self.cleaned_data
        Contact.objects.create(**data)
        send_mail(
            self.template_name, 
            subject=data['title'], 
            from_email=settings.DEFAULT_FROM_EMAIL, 
            to_email=settings.DEFAULT_TO_EMAIL_LIST,
            context=data
        )
