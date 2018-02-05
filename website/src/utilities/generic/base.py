from django.views.generic.base import TemplateView
from django.conf import settings
from django.http import Http404

class TemplateView(TemplateView):

    status = 200
    
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['page'] = self.kwargs.get('page', 1 )        
        return context

    def render_to_response(self, context, **response_kwargs):

        response_kwargs['status'] = self.status
        if  self.status == 404 and settings.TEMPLATE_DEBUG == True:
            raise Http404()
        return super(TemplateView, self).render_to_response(context, **response_kwargs)

