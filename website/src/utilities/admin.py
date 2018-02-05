from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def create_modeladmin(modeladmin, model, name=None):

    def get_model_title():
        if hasattr(modeladmin, 'Meta'):
            if hasattr(modeladmin, 'verbose_name') is None:
                return model._meta.verbose_name
            else:
                return modeladmin.Meta.verbose_name
        else:
            return model._meta.verbose_name

    def get_verbose_name_plural():
        if hasattr(modeladmin, 'Meta') :
            if hasattr(modeladmin, 'verbose_name_plural') is None:
                return model._meta.verbose_name_plural
            else:
                return modeladmin.Meta.verbose_name_plural
        else:
            return model._meta.verbose_name_plural

    class Meta:
        proxy = True
        app_label = model._meta.app_label
        verbose_name = get_model_title()
        verbose_name_plural = get_verbose_name_plural()

    attrs = {'__module__':"", 'Meta': Meta}

    newmodel = type(name, (model,), attrs)
    
    admin.site.register(newmodel, modeladmin)
    return modeladmin

class DefaultFilterMixIn(admin.ModelAdmin):
    def changelist_view(self, request, *args, **kwargs):
        

        if self.default_filters:            
            test = request.META['HTTP_REFERER'].split(request.META['PATH_INFO'])
            test2 = request.META['QUERY_STRING']

            if len(test2) == 0 and (test and test[-1] and not test[-1].startswith('?')):
#
                url = reverse('admin:%s_%s_changelist' % (self.opts.app_label, self.opts.model_name))
                filters = []
                for filter in self.default_filters:
                    key = filter.split('=')[0]
                    if not request.GET.has_key(key):
                        
                        filters.append(filter)
                
                if filters:                        
                    return HttpResponseRedirect("%s?%s" % (url, "&".join(filters)))
                
        return super(DefaultFilterMixIn, self).changelist_view(request, *args, **kwargs)



def class_gen_with_kwarg(cls, **additionalkwargs):
  """class generator for subclasses with additional 'stored' parameters (in a closure)
     This is required to use a formset_factory with a form that need additional 
     initialization parameters (see http://stackoverflow.com/questions/622982/django-passing-custom-form-parameters-to-formset)
  """
  class ClassWithKwargs(cls):
      def __init__(self, *args, **kwargs):
          kwargs.update(additionalkwargs)
          super(ClassWithKwargs, self).__init__(*args, **kwargs)
  return ClassWithKwargs