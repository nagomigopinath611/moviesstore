from django.contrib.auth.forms import UserCreationForm
#import ErrorList class to store & display validation error messages
from django.forms.utils import ErrorList
#import mark_safe function to mark a string as safe for HTML rendering
from django.utils.safestring import mark_safe

#Class to customise the way errors are displayed
class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

#New custom class CustomUserCreationForm that inherits from UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        #super method to call parent's constructor
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1',
        'password2']:
            #iterate through each field and set help_text to None
            self.fields[fieldname].help_text = None
            #add CSS form-control class to the field’s widget 
            #Bootstrap class to improve look & feel
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )