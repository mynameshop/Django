from django import forms
from django.contrib.admin import widgets
from django.forms.utils import ErrorList
from profiles.models import Party
from profiles.models import Personal
from profiles.models import Profile
from profiles.models import Proxy


class ProfileMixForm(forms.ModelForm):
    profile_name = forms.CharField()
    slug_text = forms.CharField(label='Slug')
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None):
        
        super(ProfileMixForm, self).__init__(data, files, auto_id, prefix,
                                             initial, error_class, label_suffix, empty_permitted, instance)
        
        try:
            self.profile = self.instance.profile
        except:
            self.profile = Profile(name="", slug="")
        
        self.fields['profile_name'].initial = self.profile.name
        self.fields['slug_text'].initial = self.profile.slug
        
    def save(self, commit=True):
        self.profile.name = self.cleaned_data['profile_name']
        self.profile.slug = self.cleaned_data['slug_text']
        self.profile.save()
        self.instance.profile = self.profile
        return super(ProfileMixForm, self).save(commit)    


class PersonalForm(ProfileMixForm):
    birthday = forms.DateField(widget=widgets.AdminDateWidget())
    class Meta:
        model = Personal
        fields = ['profile_name', 'slug_text', 'user', 'gender', 'birthday', ]
        
        
class ProxyForm(ProfileMixForm):
    class Meta:
        model = Proxy
        fields = ['profile_name', 'slug_text', 'proxy_only', 'created_by', ]
   
   
class PartyForm(ProfileMixForm):
    class Meta:
        model = Party
        fields = ['profile_name', 'slug_text', 'num_members', 'is_manual', 'created_by', ]
