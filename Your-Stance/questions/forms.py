from django import forms
from django.forms import ModelForm

from questions.models import SuggestedQuestion, Question

class SuggestQuestionForm(ModelForm):
    class Meta:
        model = SuggestedQuestion
        fields = ['slug', 'details', ]
    
    def clean(self):
        if 'slug' in self.cleaned_data:
            q_same_slug = Question.objects.filter(slug=self.cleaned_data['slug'])
            s_same_slug = SuggestedQuestion.objects.filter(slug=self.cleaned_data['slug'])
            
            if len(q_same_slug) or len(s_same_slug):
                self._errors['slug']='Question with such slug already exists.'
        
        
        return self.cleaned_data
        