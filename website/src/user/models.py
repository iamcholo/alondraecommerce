from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from utilities.media import write_file
from utilities.media import remove_old_file
from utilities.image_base64 import encode_image, image_exists
from django.db import models

models.options.DEFAULT_NAMES += ('show_in_admin_menu',)

class CustomUser(AbstractUser):
    logo = models.ImageField(
            _('Logo'), 
            upload_to='uploads/users/', 
            null=True, 
            blank=True
        )
    
    nick = models.CharField(
            _('NICK_LABEL'),
            max_length=255,
            unique=True,
            blank=True      
        )

    autor_info = models.TextField(
            _('About You'),
            blank=True
        )    
    def __unicode__(self):
        return '%s' % (self.username)
    
    def __init__(self, *args, **kwargs):
        super(CustomUser, self).__init__(*args, **kwargs)
        if self.logo is not None:
            self._prev_logo = self.logo

    class Meta:
        #swappable = 'AUTH_USER_MODEL'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        get_latest_by = "created"
        ordering = ('-id',)
        db_table = 'auth_custom_user'
        app_label = 'user'
        show_in_admin_menu = False

    def update_logo(self):
        instance = self
        if instance.logo is not None:
            write_file(instance.logo, instance.id)

            if len(instance._prev_logo.name)> 0:
                if instance._prev_logo.name != instance.logo.name:
                    remove_old_file(instance._prev_logo, instance.id)

            CustomUser.objects.filter(id=instance.id).update(
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
        logo = settings.STATIC_URL + "img/coment.jpg" % (width,height)      
        if len(image) and image_exists(image, self.id):
            logo = "data:image/png;base64," + encode_image( image, self.id, width, height)
        return logo
    def get_logo_comment(self):
        image = self.logo.name
        logo = settings.STATIC_URL + "img/coment.jpg" 
        if len(image) and image_exists(image, self.id):
            logo = "data:image/png;base64," + encode_image( image, self.id, width, height)
        return logo