#encoding:iso-8859-1
from django.contrib import admin
from django.contrib import messages
from django.utils.html import escape
from user_site.models import UserSite
from django.conf.urls import patterns
from django.http import HttpResponseRedirect
from django.contrib.admin.utils import unquote
from user_site.forms import UserSiteAdminForm
from django.shortcuts import get_object_or_404
from user_site.forms import UserSiteCreationForm
from django.utils.decorators import method_decorator
from django.template.response import TemplateResponse
from django.contrib.admin.options import IS_POPUP_VAR
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.views.decorators.debug import sensitive_post_parameters
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())
from django.utils.text import slugify


class UserSiteAdmin(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None

    fieldsets = [
     (_('Basic'),{'fields': [
            'first_name','last_name',
            'password',
            'email', 'is_active',
           # 'tel', 'fax',
           # 'mobile',
        ]})
    ]

    add_fieldsets = [
     (_('Basic'),{'fields': [
            'first_name','last_name',
             'password1','password2',
            'email', 'is_active',
           # 'tel', 'fax', 
           # 'mobile', 
        ]})
    ]

    list_display = (
        'email', 'id','nick','first_name','last_name',
        #'tel', 'fax', 'mobile', 
        'is_active', 'created', 'modified'
    )

    form = UserSiteAdminForm
    add_form = UserSiteCreationForm
    change_password_form = AdminPasswordChangeForm
    search_fields = ['email']

    def save_model(self, request, obj, form, change):
        email = obj.email
        to_nick = email.split('@')
        obj.nick = to_nick[0]
        obj.nick_slug = slugify(to_nick[0])
        obj.save()

    def get_urls(self):
        
        return patterns('',
            (r'^(\d+)/password/$',
            self.admin_site.admin_view(self.user_change_password))
        ) + super(UserSiteAdmin, self).get_urls()

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserSiteAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form,
                'fields': admin.utils.flatten_fieldsets(self.add_fieldsets),
            })
        defaults.update(kwargs)
        return super(
                UserSiteAdmin, 
                self
            ).get_form(request, obj, **defaults)

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):

        if not self.has_change_permission(request):
            raise PermissionDenied
    
        user = get_object_or_404(self.get_queryset(request), pk=id)
       
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, request.user, change_message)
                msg = _('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})
        context = {
            'title': _('Change password: %s') % escape(user.email),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': IS_POPUP_VAR in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True
        }
        templa=self.change_user_password_template or 'admin/auth/user/change_password.html'
        return TemplateResponse(request, templa, context, current_app=self.admin_site.name)

admin.site.register(UserSite,UserSiteAdmin)
