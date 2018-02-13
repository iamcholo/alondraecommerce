from django import forms
from navigation.models import NavigationItem, NavigationPosition
from mptt.forms import TreeNodeChoiceField
from widgets import CustomSelectWidget
from django.contrib.contenttypes.models import ContentType

class NavigationItemAdminItemForm(forms.ModelForm):
    parent = TreeNodeChoiceField( NavigationItem.objects.all().order_by('id'), required=False)
    class Meta:  
        widgets = {
            'meta_description':  forms.Textarea(attrs={'maxlength':156,}),
            'object_id': forms.Select(attrs={
                'class':'selector',
                }),
           'content_type': CustomSelectWidget(attrs={
                'class':'selector',
            }),
        }
    def __init__(self, *args, **kwargs):

        super(NavigationItemAdminItemForm, self).__init__(*args, **kwargs)


        if self.instance.id is not None:

            
            self.fields['parent'].queryset = NavigationItem.objects.filter(
                    position__id=self.instance.position.id
                ).exclude(
                    id__in=[self.instance.id]+[item.id for item in self.instance.get_descendants()]
                ).order_by('id')
            
            obj = ContentType.objects.get_for_id(self.instance.content_type.id)
            choices = [ ( x.id,  x.title_name()) for  x in obj.model_class().get_items_navigation()]
            self.fields['object_id'].widget.choices = choices


class NavigationItemAdminItemForm2(NavigationItemAdminItemForm):
    def __init__(self, *args, **kwargs):


        self._xexclude_id = kwargs.pop('xexclude_id', None)
        
        super(NavigationItemAdminItemForm2, self).__init__(*args, **kwargs)

        
        if self.instance.id is not None:
            
            self.fields['parent'].queryset = NavigationItem.objects.filter(
                    position__id=self.instance.position.id
                ).exclude(
                    id__in=[self.instance.id]+[item.id for item in self.instance.get_descendants()]
                ).order_by('id')
            
            obj = ContentType.objects.get_for_id(self.instance.content_type.id)
            choices = [ ( x.id,  x.title_name()) for  x in obj.model_class().get_items_navigation()]
            self.fields['object_id'].widget.choices = choices
        else:
            if self._xexclude_id is not None:
                self.fields['parent'].queryset = NavigationItem.objects.filter(
                        position__id=self._xexclude_id 
                    ).order_by('id')
                self.fields['position'].queryset = NavigationPosition.objects.filter(
                        id=self._xexclude_id 
                    )
                self.fields['position'].initial = self._xexclude_id 


class EditNavigationItemAdminItemForm(NavigationItemAdminItemForm):
    class Meta: 
        exclude = ('position',) # this doesn't work, due to the way 


