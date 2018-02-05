from django.conf import settings
from django.db import models
from django.core import validators
from django.core.mail import send_mail
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
#from django_countries.fields import CountryField
from django.db.models.signals import post_save
from utilities.media import write_file
from utilities.media import remove_old_file
from utilities.image_base64 import encode_image, image_exists
from django.utils.text import slugify
from django.conf import settings

class UserSiteManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)   
        user = self.model(                    
                    email=email,                 
                    is_active=True,                           
                    *extra_fields
                )
        if password is None:
            password = UserSite.objects.make_random_password()
        user.set_password(password)
        
        user.save(using=self._db)
        
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user( email, password,**extra_fields)

class UserSite(AbstractBaseUser):   
    
    first_name = models.CharField(_('First Name'), max_length=32, null=True, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=32, null=True, blank=True)
    email = models.EmailField(_('email address'))
    is_active = models.BooleanField(
            _('active'), 
            default=True,
            help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
        )
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserSiteManager()

    def __unicode__(self):
        return '%s - %s' % (self.nick, self.email)
    
    def __init__(self, *args, **kwargs):
        super(UserSite, self).__init__(*args, **kwargs)
        if self.logo is not None:
            self._prev_logo = self.logo


    class Meta:
        verbose_name = _('User Site')
        verbose_name_plural = _('User Site')
        get_latest_by = "created"
        ordering = ('-id',)
        db_table = 'auth_user_site'
        app_label= 'auth'

    def update_logo(self):
        instance = self
        if instance.logo is not None:
            write_file(instance.logo, instance.id)

            if len(instance._prev_logo.name)> 0:
                if instance._prev_logo.name != instance.logo.name:
                    remove_old_file(instance._prev_logo, instance.id)

            UserSite.objects.filter(id=instance.id).update(
                    logo=instance.logo
                )
    
    def get_logo(self, width=38, height=38):
        image = self.logo.name
        logo = settings.STATIC_URL + "images/avatar-%s-%s.png" % (width,height)      
        if len(image) and image_exists(image, self.id):
            logo = "data:image/png;base64," + encode_image( image, self.id, width, height)
        return logo
        
    def get_logo60x60(self,width=60,height=60):
        image = self.logo.name
        logo = settings.STATIC_URL + "images/avatar-%s-%s.png" % (width,height)      
        if len(image) and image_exists(image, self.id):
            logo = "data:image/png;base64," + encode_image( image, self.id, width, height)
        return logo
