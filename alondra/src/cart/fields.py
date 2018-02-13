from django.forms.fields import MultipleChoiceField 
from django.forms.widgets import Widget
from django.utils.datastructures import MultiValueDict

class MyTypedMultipleChoiceField(MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        self.coerce = kwargs.pop('coerce', lambda val: val)
        self.empty_value = kwargs.pop('empty_value', [])
        super(MyTypedMultipleChoiceField, self).__init__(*args, **kwargs)
    def to_python(self, value):
        """
        Validates that the values are in self.choices and can be coerced to the
        right type.
        """
        value = super(MyTypedMultipleChoiceField, self).to_python(value)
        new_value = []
       
        for choice in value:
            if len(choice) > 0:
                new_value.append(self.coerce(int(choice)))      
        return new_value
    def validate(self, value):
        pass

class MyHiddenListInput(Widget):
    input_type = 'hidden'
    is_hidden = True
    def __init__(self, attrs=None):
        if attrs is not None:
            self.input_type = attrs.pop('type', self.input_type)
        super(MyHiddenListInput, self).__init__(attrs)

    def value_from_datadict(self, data, files, name):
        
        return data.getlist(name)
#        return  

class MyTextListInput(Widget):
    input_type = 'text'

    def __init__(self, attrs=None):
        if attrs is not None:
            self.input_type = attrs.pop('type', self.input_type)
        super(MyTextListInput, self).__init__(attrs)

    def value_from_datadict(self, data, files, name):
        return data.getlist(name)