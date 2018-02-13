#utf-8
import re
from django import template
from html2text import HTML2Text
from pygments import highlight
from bs4 import BeautifulSoup, Tag
from pygments.formatters import HtmlFormatter
from django.utils.html import format_html
from pygments.lexers import get_lexer_by_name, guess_lexer

register = template.Library()
regex = re.compile('\[([^]]+)\]')



@register.filter
def pygmentize(content, replace_parent=False):

    soup = BeautifulSoup(unicode(content))
    columns = soup.findAll(u'code')
    formatter = HtmlFormatter(cssclass=u'source', linenos=True)
    for code in columns:
        lang = u'text'
       
        if code.has_attr(u'class'):

            lang = next(iter( code[u'class']), u'text').lower()
            try:
                lexer = get_lexer_by_name(lang, stripnl=True, encoding=u'UTF-8')
            except ValueError, e:
                lexer = get_lexer_by_name(u'text', stripnl=True, encoding=u'UTF-8')

            new_html = BeautifulSoup(highlight( code.renderContents(), lexer, formatter))
            if replace_parent:
                code.parent.replaceWith(new_html)
            else:
                code.replaceWith(new_html)
           
    return unicode(soup)

@register.filter
def image_short_code(content,replace_parent=False):
    soup = BeautifulSoup(unicode(content))
    columns = soup.findAll(text =regex)
    for code in columns:
        pattern = re.search(r'\[IMG(.*?)\]',code)
        if pattern:
            tag = Tag(soup,"img")
            tag['src'] = re.sub(r'\[IMG(.*?)\]|\[\/IMG\]','',code)
            for attr in re.findall(r'(\w+\=\d+)',pattern.group(0)):
                name,val = attr.split('=')
                tag[name] = val
            
            if replace_parent:

                code.parent.replaceWith(tag)
            else:
                code.replaceWith(tag)
    return unicode(soup)

@register.filter
def iframe_short_code(content, replace_parent=False):
    soup = BeautifulSoup(unicode(content))
    columns = soup.findAll(text =regex)
    for code in columns:
        pattern = re.search(r'\[IFRAME(.*?)\]',code)
        if pattern:
            tag = soup.new_tag('iframe')
            div = soup.new_tag('div')
            div['class'] = "videoWrapper"
            tag['src'] = re.sub(r'\[IFRAME(.*?)\]|\[\/IFRAME\]','',code)
            tag['frameborder'] = 0
            tag['allowfullscreen'] = True
            
            for attr in re.findall(r'(\w+\=\d+)',pattern.group(0)):
                name,val = attr.split('=')
                tag[name] = val
            div.append(tag)
            if replace_parent:
                code.parent.replaceWith(div)
            else:
                code.replaceWith(div)
    return  unicode(soup) 



