#encoding:utf-8
import os
import json
import codecs
from django import forms
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _


class GlobalConfigForm(forms.Form):
    sitename = forms.CharField(label= _('Site Name'), max_length=255,required=True)
    sitelink = forms.CharField(label= _('Site Link Url'), max_length=255,required=True)
    metatitle = forms.CharField(label= _('Meta Title'), max_length=70,required=True)
    metadescription = forms.CharField(
            label=_('Meta Description'),
            widget=forms.Textarea(attrs={'maxlength': 155}),
            max_length=155,
            required=True
        )
    def __init__(self, *args, **kwargs):
        super(GlobalConfigForm, self).__init__(*args, **kwargs)
        #open file
        if (os.path.isfile(settings.GLOBAL_CONFIG_FILE) 
            and os.access(settings.GLOBAL_CONFIG_FILE, os.R_OK)):
            with open(settings.GLOBAL_CONFIG_FILE,'r') as data_file:
                try:
                    data = json.load(data_file)                 
                    if data.has_key('sitename'):
                        self.fields['sitename'].initial = data['sitename']

                    if data.has_key('sitelink'):
                        self.fields['sitelink'].initial = data['sitelink']

                    if data.has_key('metatitle'):
                        self.fields['metatitle'].initial = data['metatitle']

                    if data.has_key('metadescription'):
                        self.fields['metadescription'].initial = data['metadescription']
                except ValueError:
                    pass
            data_file.close()


    def get_template(self, **context):
        TEMPLATE_FILE = 'global_config/config_template.json'
        d = Context(context)
        plaintext = get_template(TEMPLATE_FILE)
        return plaintext.render(d)
    def save(self):
        if (os.path.isfile(settings.GLOBAL_CONFIG_FILE) 
            and os.access(settings.GLOBAL_CONFIG_FILE, os.R_OK)):
            fd = codecs.open(settings.GLOBAL_CONFIG_FILE, "w", "utf-8")
            fd.write(self.get_template(**self.cleaned_data))
            fd.close()
