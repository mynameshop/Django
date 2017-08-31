from datetime import datetime
from django import forms
from  django.utils.html import format_html
from django.contrib.auth.models import User
from profiles.models import ProfileVerification


        
class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class EditProfileForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    name = forms.CharField(label='Name', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    location = forms.CharField(label='Location', max_length=100, required=False)
    bio = forms.CharField(label='Bio', widget=forms.Textarea, required=False)


class NotificationsForm(forms.Form):
#    replies = forms.BooleanField(label='Replies', required=False)
#    agrees = forms.BooleanField(label='Agree', required=False)
    question = forms.BooleanField(label='Replies', required=False)
    follower = forms.BooleanField(label='Replies', required=False)
    agrees = forms.BooleanField(label='Replies', required=False)
    comment = forms.BooleanField(label='Replies', required=False)
    mention = forms.BooleanField(label='Replies', required=False)
    like = forms.BooleanField(label='Replies', required=False)


class VerificationForm(forms.ModelForm):
    class Meta:
        model = ProfileVerification
        fields = ['photo', ]
        widgets = {
            'photo': forms.FileInput()
        }

        
    def save(self):
        self.instance.status = ProfileVerification.STATUS_PENDING
        super(VerificationForm, self).save()