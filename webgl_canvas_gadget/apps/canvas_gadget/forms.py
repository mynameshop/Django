from __future__ import unicode_literals
from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction
from multiupload.fields import MultiFileField
from apps.projects.models import Project

from .models import ProjectRequest, ProjectRequestImage

class ProjectRequestForm(forms.ModelForm):
    user = forms.IntegerField(required=False, widget=forms.HiddenInput())
    project_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Project Name'}))
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': u'Email Address'}))
    project_description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': u'Short description of your product', 'rows':6})
    )
    subscription_template = forms.IntegerField(widget=forms.HiddenInput())
    images = MultiFileField(
        min_num=0, 
        max_num=10, 
        max_file_size=1024*1024*13, 
        required=False,
    )
    class Media:
        js = {}
        
    class Meta:
        model = ProjectRequest
        exclude = ['created_at', 'project', 'status',]
        fields = ['user', 'subscription_template', 'project_name', 'user_email','images', 'project_description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs['initial'].get('user', None):
            self.fields['user_email'].widget = forms.HiddenInput()
        for f in self.visible_fields():
            if f.name == 'images':
                self.fields[f.name].widget.attrs['class'] = 'hidden uploader'
                continue
            self.fields[f.name].widget.attrs['class'] = 'form-control'
    
    @transaction.atomic        
    def save_all(self): 
        obj = self.save()
        for img in self.cleaned_data['images']:
            ProjectRequestImage.objects.create(
                project_request=obj,
                image=img
            )
        return obj
    
    def clean_user(self):
        user = self.cleaned_data['user']
        if user:
            user = get_user_model().objects.get(id = user)
        return user
    
    def clean_user_email(self):
        user_email = self.cleaned_data['user_email']
        user = self.cleaned_data['user']
        if not user and user_email:
            if get_user_model().objects.filter(username = user_email).exists():
                msg = u'User with the same email address already exists. Please login or use other email address.'
                self.add_error('user_email', msg)
        return user_email