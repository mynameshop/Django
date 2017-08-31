from django import forms
from profiles.models import Profile, ProfileVerification
from django.utils.safestring import mark_safe

from profiles import validation_helper as vh

class VerificationPhotoWidget(forms.FileInput):
    def __init__(self, attrs={}):
        super(VerificationPhotoWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s">'
                           '<img src="%s" style="width: 128px;" /></a> '
                           % (value.url, value.url)))
        output.append(super(VerificationPhotoWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class VerificationAdminForm(forms.ModelForm):
    class Meta:
        model = ProfileVerification
        fields = [ 'photo', 'status', ]
        widgets = {
            'photo': VerificationPhotoWidget()
        }
        

class FbWedgeForm(vh.ValidateUsernameMixin, forms.Form):
    username = forms.CharField(max_length=128, required=True)
    display_name = forms.CharField(max_length=128, required=True)
    verification = forms.FileField(required=True)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())
    
    def set_user(self, user):
        self.user = user
    
    def clean(self):
        self.validate_username(self.user)
    
    
                 
    
    