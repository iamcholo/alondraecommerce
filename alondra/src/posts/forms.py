from django import forms
from media.widgets import MediaItemWidget,MediaContentWidget
from posts.models import PostItem
from posts.models import PostCategory
from mptt.forms import TreeNodeChoiceField

class SearchForm(forms.Form):
	q = forms.CharField(max_length=255)
	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
		self.fields['q'].required = False

class PostItemAdminForm(forms.ModelForm):

    class Meta:  
        widgets = {
            'content':  MediaContentWidget(attrs={ 'v-model':"input",'debounce':"300"}),
        	'thumbnail': MediaItemWidget(),
        	'featured_image': MediaItemWidget(), 
            'meta_description':  forms.Textarea,        
        }
    
    def __init__(self, *args, **kwargs):
        super(PostItemAdminForm, self).__init__(*args, **kwargs)
        self.fields['related_posts'].queryset = PostItem.objects.exclude(
                id__exact=self.instance.id
            )

class PostArticleAdminForm(PostItemAdminForm):

    def __init__(self, *args, **kwargs):
        super(PostArticleAdminForm, self).__init__(*args, **kwargs)
        self.fields['related_posts'].queryset = PostItem.objects.filter(
                post_type="post"
            ).exclude(
                id__exact=self.instance.id,                
            )
        self.fields['categories'].queryset = PostCategory.objects.filter(
                post_type="post"
            )

class PostPageAdminForm(PostItemAdminForm):

    def __init__(self, *args, **kwargs):
        super(PostPageAdminForm, self).__init__(*args, **kwargs)
        self.fields['related_posts'].queryset = PostItem.objects.filter(
                post_type="page"
            ).exclude(
                id__exact=self.instance.id,                
            )
        self.fields['categories'].queryset = PostCategory.objects.filter(
                post_type="page"
            )

class PostVideoAdminForm(PostItemAdminForm):

    def __init__(self, *args, **kwargs):
        super(PostVideoAdminForm, self).__init__(*args, **kwargs)
        self.fields['related_posts'].queryset = PostItem.objects.filter(
                post_type="video"
            ).exclude(
                id__exact=self.instance.id,
            )
        self.fields['categories'].queryset = PostCategory.objects.filter(
                post_type="video"
            )

class PostCategoryAdminArticleForm(forms.ModelForm):
    parent = TreeNodeChoiceField( PostCategory.objects.filter(
                post_type="post"
            ),required=False)
    class Meta:  
        widgets = {
          'meta_description':  forms.Textarea(
            attrs={
                'maxlength':156,
                #'data-url': reverse("navigation_get_item"),
            }),
        }

    def __init__(self, *args, **kwargs):
        super(PostCategoryAdminArticleForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = PostCategory.objects.filter(
                post_type="post"
            ).exclude(
                id__exact=self.instance.id,
            )

class PostCategoryAdminPageForm(PostCategoryAdminArticleForm):
    def __init__(self, *args, **kwargs):
        super(PostCategoryAdminPageForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = PostCategory.objects.filter(
                post_type="page"
            ).exclude(
                id__exact=self.instance.id,
            )

class PostCategoryAdminVideoForm(PostCategoryAdminArticleForm):
    def __init__(self, *args, **kwargs):
        super(PostCategoryAdminVideoForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = PostCategory.objects.filter(
                post_type="video"
            ).exclude(
                id__exact=self.instance.id,
            )