from django import forms
from django.forms import ModelForm

from .models import Stance

CHOICES=[('p',''),
         ('c',''),
         ('u','')]

class NewStanceForm(ModelForm):
    choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), label='')
    class Meta:
        model = Stance
        fields = ['stance_text', 'question']
        widgets = {
            'question': forms.HiddenInput(),
        }


class EditStanceForm(ModelForm):

    class Meta:
        model = Stance
        fields = ['stance_text']



class ReplyStanceForm(ModelForm):

    class Meta:
        model = Stance
        fields = ['stance_text' ]
        widgets = {'stance_text': forms.Textarea(attrs={'class': 'stanceReplyForm'})}
