from __future__ import unicode_literals

from django import forms
from captcha.fields import ReCaptchaField
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    captcha = ReCaptchaField(attrs={'callback':'enableSubmitButton', 'expired-callback': 'disableSubmitButton'})
    
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'phone', 'website', 'text', 'captcha']