#encoding:utf-8
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

def send_mail(template, subject, from_email, to_email=[],context = {}):
    d = Context(context)
    plaintext = get_template('email/%s.txt' % template)
    htmly     = get_template('email/%s.html' % template)    
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()