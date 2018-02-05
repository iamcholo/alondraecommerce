from django.utils.safestring import mark_safe
from django.forms import widgets
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext_lazy as _

# your custom widget class
class MediaItemWidget(widgets.TextInput):
    def render(self, name, value, attrs={None}):
        text_title = _('SELECT_FILE_IMAGE_LABEL')
        mediamanager_url = reverse("admin:media_mediaimage_changelist")
    	myfield = u'<a href="%s?_popup=1" style="vertical-align:top; display:inline-block; margin: 0px .7em ; background:#7CA0C7; color: white; padding: 10px;" id="%s"  class="selectmediaItem btn btn-primary"><i class="icon-search icon-white"></i> %s</a>&nbsp;' % (mediamanager_url, name, text_title)
        return mark_safe(u''' %s %s''' 
        	% (myfield, super(MediaItemWidget, self).render(name, value, attrs)))

class MediaContentWidget(widgets.Textarea):
    def render(self, name, value, attrs={None}):
        
        text_title = _('SELECT_MEDIA_IMAGE_LABEL')
        album_title = _('SELECT_MEDIA_ALBUM_LABEL')
        mediamanager_url = reverse("admin:media_mediaimage_changelist")
        mediaalbum_url = reverse("admin:media_mediaalbum_changelist")
    	myfield = u'<a href="%s?_popup=1" style="vertical-align:top; display:inline-block; margin: .7em; background:#7CA0C7; color: white; padding: 10px;" id="%s"  class="selectmediaItem  btn btn-primary"><i class="icon-search icon-white"></i> %s</a>&nbsp;' % (mediamanager_url, name, text_title)
        mediaalbum_myfield = u'<a href="%s?_popup=1" style="vertical-align:top; display:inline-block; margin: .7em; background:#7CA0C7; color: white; padding: 10px;" id="%s"  class="InsertAlbum  btn btn-primary"><i class="icon-search icon-white"></i> %s</a>&nbsp;' % (mediaalbum_url, name, album_title)
        attrs.update({
            "data-media-image-url":mediamanager_url+'?_popup=1',
            "data-media-album-url":mediaalbum_url+'?_popup=1'
        })
        #return mark_safe(u'''
        #        <div class="editors">
        #            <div id="editor" class="editor"> 
        #                %s 
        #                
        #            </div>
        #            
        #        </div>
        #        
        #         %s %s''' 
        #	% ( super(MediaContentWidget, self).render(name, value, attrs), myfield, mediaalbum_myfield))
        return mark_safe(u'''
                <div class="editors">
                    <div id="editor" class="editor"> 
                        %s 
                        
                    </div>
                    
                </div>                
                ''' 
            % ( super(MediaContentWidget, self).render(name, value, attrs)))
