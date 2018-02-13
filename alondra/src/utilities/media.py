import re
import json
import os
import sys
import uuid
import StringIO
from PIL import Image, ImageOps
from urlparse import urlparse
from django.conf import settings
from bs4 import BeautifulSoup, Tag
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


def write_file(filename, pk):
    #save the the new filename
    oldfile = filename.name
    ext = oldfile.rfind('.')
    key = str(pk)
    new_name = "%s%s" % (uuid.uuid4(),oldfile[ext:])
    new_path = ('%s/%s' %(key, new_name))
    source = filename.path
    directory_path = "%s%s" % (settings.MEDIA_ROOT, 'uploads/')
    destination = os.path.join(
            directory_path, 
            new_path
        )
    
    directory = os.path.join(
            directory_path,
            key
        )
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.isfile(source):
        os.rename(source, destination)
        filename.name = new_name

def remove_old_file(filename, pk):
    #save the the new filename
    directory_path = "%s%s" % (settings.MEDIA_ROOT, 'tmp/')
    source = os.path.join(
            directory_path, 
            ('%s/%s' %(str(pk), filename.name))
        )
    if os.path.isfile(source):
        os.remove(source)




oembed_urls = {
    
    'http://((m|www)\.)?youtube\.com/watch.*'         : ['http://www.youtube.com/oembed?url={url}&format={format}', True],
    'https://((m|www)\.)?youtube\.com/watch.*'        : ['http://www.youtube.com/oembed?scheme=https&url={url}&format={format}', True],
    'http://((m|www)\.)?youtube\.com/playlist.*'      : ['http://www.youtube.com/oembed?url={url}&format={format}', True],
    'https://((m|www)\.)?youtube\.com/playlist.*'     : ['http://www.youtube.com/oembed?scheme=https?url={url}&format={format}', True],
    'http://youtu\.be/.*'                             : ['http://www.youtube.com/oembed?url={url}&format={format}', True],
    'https://youtu\.be/.*'                            : ['http://www.youtube.com/oembed?scheme=https&url={url}&format={format}', True],
    'https?://(.+\.)?vimeo\.com/.*'                   : ['http://vimeo.com/api/oembed.{format}?url={url}&format={format}', True],
    'https?://(www\.)?dailymotion\.com/.*'            : ['https://www.dailymotion.com/services/oembed?url={url}&format={format}', True],
    'http://dai.ly/*'                                 : ['https://www.dailymotion.com/services/oembed?url={url}&format={format}', True],
    'https?://(www\.)?flickr\.com/.*'                 : ['https://www.flickr.com/services/oembed/?url={url}&format={format}', True],
    'https?://flic\.kr/.*'                            : ['https://www.flickr.com/services/oembed/?url={url}&format={format}', True],
    'https?://(.+\.)?smugmug\.com/.*'                 : ['http://api.smugmug.com/services/oembed/?url={url}&format={format}', True],
    'https?://(www\.)?hulu\.com/watch/.*'             : ['http://www.hulu.com/api/oembed.{format}?url={url}&format={format}', True],
    'http://i*.photobucket.com/albums/*'              : ['http://api.photobucket.com/oembed?url={url}&format={format}',True],
    'http://gi*.photobucket.com/groups/*'             : ['http://api.photobucket.com/oembed?url={url}&format={format}',True],
    'https?://(www\.)?scribd\.com/doc/.*'             : ['http://www.scribd.com/services/oembed?url={url}&format={format}',True],
    'https?://wordpress.tv/.*'                        : ['http://wordpress.tv/oembed/?url={url}&format={format}',True],
    'https?://(.+\.)?polldaddy\.com/.*'               : ['https://polldaddy.com/oembed/?url={url}&format={format}',True],
    'https?://poll\.fm/.*'                            : ['https://polldaddy.com/oembed/?url={url}&format={format}',True],
    'https?://(www\.)?funnyordie\.com/videos/.*'      : ['http://www.funnyordie.com/oembed?url={url}&format={format}',True],
    'https?://(www\.)?twitter\.com/.+?/status(es)?/.*': ['https://api.twitter.com/1/statuses/oembed.{format}?url={url}&format={format}',True],
    'https?://vine.co/v/.*'                           : ['https://vine.co/oembed.{format}?url={url}&format={format}',True],
    'https?://(www\.)?soundcloud\.com/.*'             : ['http://soundcloud.com/oembed?url={url}&format={format}',True],
    'https?://(.+?\.)?slideshare\.net/.*'             : ['https://www.slideshare.net/api/oembed/2?url={url}&format={format}',True],
    'https?://(www\.)?instagr(\.am|am\.com)/p/.*'     : ['https://api.instagram.com/oembed?url={url}&format={format}', True],
    'https?://(www\.)?rdio\.com/.*'                   : ['http://www.rdio.com/api/oembed/?url={url}&format={format}',True],
    'https?://rd\.io/x/.*'                            : ['http://www.rdio.com/api/oembed/?url={url}&format={format}',True],
    'https?://(open|play)\.spotify\.com/.*'           : ['https://embed.spotify.com/oembed/?url={url}&format={format}', True],
    'https?://(.+\.)?imgur\.com/.*'                   : ['http://api.imgur.com/oembed?url={url}&format={format}',True],
    'https?://(www\.)?meetu(\.ps|p\.com)/.*'          : ['http://api.meetup.com/oembed?url={url}&format={format}',True],
    'https?://(www\.)?issuu\.com/.+/docs/.+#i'        : ['http://issuu.com/oembed_wp?url={url}&format={format}',True],
    'https?://(www\.)?collegehumor\.com/video/.*'     : ['http://www.collegehumor.com/oembed.{format}?url={url}&format={format}',True],
    'https?://(www\.)?mixcloud\.com/.*'               : ['http://www.mixcloud.com/oembed?url={url}&format={format}', True],
    'https?://(www\.|embed\.)?ted\.com/talks/.*'      : ['http://www.ted.com/talks/oembed.{format}?url={url}&format={format}', True],
    'https?://(www\.)?(animoto|video214)\.com/play/.*': ['https://animoto.com/oembeds/create?url={url}&format={format}', True],
    'https?://(.+)\.tumblr\.com/post/.*'              : ['https://www.tumblr.com/oembed/1.0?url={url}&format={format}', True],
    'https?://(www\.)?kickstarter\.com/projects/.*'   : ['https://www.kickstarter.com/services/oembed?url={url}&format={format}',True],
    'https?://kck\.st/.*'                             : ['https://www.kickstarter.com/services/oembed?url={url}&format={format}',True],
    'https?://cloudup\.com/.*'                        : ['https://cloudup.com/oembed?url={url}&format={format}',True],
    'https?://(www\.)?reverbnation\.com/.*'           : ['https://www.reverbnation.com/oembed?url={url}&format={format}',True],
#    'https?://videopress.com/v/.*#'                  : ['https://public-api.wordpress.com/oembed/1.0/?for={url}' ,True],
    'https?://(www\.)?reddit\.com/r/[^/]+/comments/.*': ['https://www.reddit.com/oembed?url={url}&format={format}',True],
    'https?://(www\.)?speakerdeck\.com/.*'            : ['https://speakerdeck.com/oembed.{format}?url={url}&format={format}',True],
    'https?://(mobile|www\.)?twitter\.com/.*'         : ['https://api.twitter.com/1/statuses/oembed.json?url={url}',False],

}

regex = re.compile(r'|'.join(oembed_urls.keys()))
path =  re.compile(r'([a-zA-Z0-9_\-]{4,})')
img_tag_regex =  re.compile(r'(\<img([\w\W]+?)\/\>)')


def surf(url):
    
    user_agent = {'User-agent': 'Mozilla/5.0'}
    return requests.get(url,  headers = user_agent, verify=False).content

def get_oembed_url(url):
   
    for key,value in oembed_urls.items():        
        if re.match(key, url): 
            return value
    return None

def get_img_tag(tag):
   
    
    if re.match(img_tag_regex, tag): 
        return value
    return None


def add_img_class(item,classname=['img-responsive']):
    soup = BeautifulSoup(unicode(item))
    columns = soup.findAll('img')   
    
    for img_tag in columns:
        print 
        img_tag['class'] = img_tag.get('class', []) + classname
   
    return unicode(soup) 

def get_oembed_html(href):
    url, is_content = get_oembed_url(href)
    oembed_url = url.format(**{
        "url": href,
        'format': 'json'
    })
    return json.loads(surf(oembed_url))

def get_oembed(item):
    
    soup = BeautifulSoup(unicode(item))
    columns = soup.findAll('a', href = regex)   
    for c in columns:
        href = c['href']
        url, is_content = get_oembed_url(href)
        if url is not None:
  
            parsed_uri = urlparse(href)
            
            domain = re.search(
                path, '{uri.hostname}'.format(
                        uri=parsed_uri
                    )
                ).group(1)

            html = get_oembed_html(href)
            html = BeautifulSoup(html.get('html'))
            div = soup.new_tag('div')
            if not is_content:
                div['class'] = "ContentWrapper %s" % domain
            else:
                div['class'] = "videoWrapper %s" % domain
            div.append(html)
            c.parent.replaceWith(div)

    return  unicode(soup)  