from django import forms
from comments.models import Comments
from captcha.fields import ReCaptchaField
from django.contrib.contenttypes.models import ContentType

class CommentsModelForm(forms.ModelForm):
    captcha = ReCaptchaField( use_ssl=True)
    class Meta:
        model = Comments
        exclude = [
            'content_object',
            'autor_content_type',
            'autor_object_id',
            'publish',
            'parent',
            'status',
            'target',
            'ip',
            'post_type',
        ]
    
    def __init__(self, *args, **kwargs):
        self._autor = kwargs.pop('autor', None)
        self._parent = kwargs.pop('parent', None)
        self._target = kwargs.pop('target', None)
        self._ip = kwargs.pop('ip', None)

        super(CommentsModelForm, self).__init__(*args, **kwargs)

        if self.instance.id is None:
            self.instance.target = self._target
            if  self._autor is not None:
                autor = ContentType.objects.get_for_model(self._autor)    
                self.instance.content_type = autor.model_class()
                self.instance.object_id = self._autor.id

                

    def save(self, commit=True):
        m = super(CommentsModelForm, self).save(commit=commit)
        if commit:
            m.ip = self._ip
            print  self._parent
            if self._parent is not None:
                try:
                    m.parent = Comments.objects.get(pk=int(self._parent)) 
                except Comments.DoesNotExist:
                    m.parent = None 
            m.save()
        return m
        