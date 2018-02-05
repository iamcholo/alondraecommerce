import json
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils import timezone
from utilities.paginator import paginator
from utilities.network import get_client_ip
from django.shortcuts import get_object_or_404
from comments.forms import CommentsModelForm
from user_site.decorators import login_required
from posts.models import PostItem
from comments.models import Comments
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
"""
    implementar google capcha
"""

def post_comment_ajax(request, id, parent=None):
    context = {'success': False,'comment':{}}
    post = get_object_or_404(PostItem, pk=int(id))
    if request.user.is_authenticated() or request.user_site.is_authenticated() :
        ip = get_client_ip(request)
        if request.user.is_authenticated():
            autor = request.user
        else:
            autor = request.user_site
        if request.method == "POST":
            x = request.POST
            form = CommentsModelForm(
                autor=autor,
                ip=ip,
                parent=parent,
                target=post,
                data=x
            )
            if form.is_valid():
                m = form.save()
                context['success'] = True
                context['comment'] = {
                    'logo': autor.get_logo(64,64),
                    'message': m.comment,
                    'publish_date': m.created.strftime("%Y-%m-%d %H:%M:%S"),
                    'modify_date': m.modified.strftime("%Y-%m-%d %H:%M:%S"),
                }
            else:
                messages.add_message(request, messages.WARNING, _('AN_ERROR_OCURRED_LABEL'))

    return HttpResponse(json.dumps(context), content_type="application/json")

def post_comment(request, id, parent=None):
    redirect_to = request.REQUEST.get('next', '')
    post = get_object_or_404(PostItem, pk=int(id))
    if request.user.is_authenticated() or request.user_site.is_authenticated() :
        ip = get_client_ip(request)
        if request.user.is_authenticated():
            autor = request.user
        else:
            autor = request.user_site
        if request.method == "POST":
            x = request.POST
            form = CommentsModelForm(
                autor=autor,
                ip=ip,
                parent=parent,
                target=post,
                data=x
            )
            
            if form.is_valid():
                m = form.save()
            else:
                messages.add_message(request, messages.WARNING, _('AN_ERROR_OCURRED_LABEL'))
                                
    return HttpResponseRedirect(redirect_to)

def edit_post_comment_ajax(request, id, post_id):
    context = {'success': False,'comment':{}}

    if request.user.is_authenticated() or request.user_site.is_authenticated() :
        ip = get_client_ip(request)

        if request.user.is_authenticated():
            autor = request.user
        else:
            autor = request.user_site

        model = ContentType.objects.get_for_model(autor)    

        comment = get_object_or_404(
            Comments, 
            pk=int(id), 
            content_type=model.model_class(),
            autor_object_id=model.id,
            target__id=int(post_id)
        )
        if request.method == "POST":
            x = request.POST
            form = CommentsModelForm(
                data=x,
                ip=ip,
                instance=comment
            )
            if form.is_valid():
                m = form.save()
                context['success'] = True
                context['comment'] = {
                    'logo': autor.get_logo(64,64),
                    'message': m.comment,
                    'publish_date': m.created.strftime("%Y-%m-%d %H:%M:%S"),
                    'modify_date': m.modified.strftime("%Y-%m-%d %H:%M:%S"),
                }

    return HttpResponse(json.dumps(context), content_type="application/json")

def edit_post_comment(request, id, post_id):
    redirect_to = request.REQUEST.get('next', '')

    if request.user.is_authenticated() or request.user_site.is_authenticated() :
        ip = get_client_ip(request)
        if request.user.is_authenticated():
            autor = request.user
        else:
            autor = request.user_site
        
        model = ContentType.objects.get_for_model(autor)    

        comment = get_object_or_404(
            Comments, 
            pk=int(id), 
            content_type=model.model_class(),
            autor_object_id=model.id,
            target__id=int(post_id)
        )
        if request.method == "POST":
            x = request.POST
            form = CommentsModelForm(
                data=x,
                ip=ip,
                instance=comment
            )
            if form.is_valid():
                m = form.save()

        if request.method == "POST":

            if form.is_valid():
                m = form.save()
                
    return HttpResponseRedirect(redirect_to)

def delete_post_comment_ajax(request, id, post_id):
    context = {'success': False}
    if request.user.is_authenticated() or request.user_site.is_authenticated():
        if request.user.is_authenticated():
            autor = request.user
        else:
            autor = request.user_site

        model = ContentType.objects.get_for_model(autor)    

        comment = get_object_or_404(
            Comments, 
            pk=int(id), 
            content_type=model.model_class(),
            autor_object_id=model.id,
            target__id=int(post_id)
        )
        context['success'] = True

    return HttpResponse(json.dumps(context), content_type="application/json")

def delete_post_comment(request, id, post_id):
    redirect_to = request.REQUEST.get('next', '')

    if request.user.is_authenticated() or request.user_site.is_authenticated():
        if request.user.is_authenticated():
            autor = request.user
        else:
            autor = request.user_site

        model = ContentType.objects.get_for_model(autor)    

        comment = get_object_or_404(
            Comments, 
            pk=int(id), 
            content_type=model.model_class(),
            autor_object_id=model.id,
            target__id=int(post_id)
        )
        
    return HttpResponseRedirect(redirect_to)

def get_comments_ajax(request, id, page=1):
    post = get_object_or_404(PostItem, pk=int(id))
    context = {'comments':[]}
    
    for comment in paginator(
            page,
            Comments.objects.filter(target=post,status='published')
        ):
        c = {
            'logo': comment.autor.get_logo(64,64),
            'message': comment.comment,
            'publish_date': comment.created.strftime("%Y-%m-%d %H:%M:%S"),
            'modify_date': comment.modified.strftime("%Y-%m-%d %H:%M:%S"),
            'level': comment.level,
            
        }
        context['comments'].append(c)
    
    return HttpResponse(json.dumps(context), content_type="application/json")

def get_comments(request, id, page=1):
    post = get_object_or_404(PostItem, pk=int(id))
    context = {'comments':[]}
    
    for comment in paginator(
            page,
            Comments.objects.filter(target=post,status='published')
        ):
        c = {
            'logo': comment.autor.get_logo(64,64),
            'message': comment.comment,
            'publish_date': comment.created.strftime("%Y-%m-%d %H:%M:%S"),
            'modify_date': comment.modified.strftime("%Y-%m-%d %H:%M:%S"),
        }
        context['comments'].append(c)
    template_name =  [
            'modules/comments/%s-post-%d.html' % (post.post_type, post.id),
            'modules/comments/%s-post-%s.html' % (post.post_type, post.slug),
            'modules/comments/%s-post.html' % post.post_type,
            'modules/comments/comments.html' 
        ] 
    return TemplateResponse(request, template_name, context)