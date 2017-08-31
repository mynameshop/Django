from django import forms


class NewThreadForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'size': '70'}))
    comment_text = forms.CharField(widget=forms.Textarea(attrs={'style': 'height:400px', 'cols': "80"}))


class ReplyThreadForm(forms.Form):
    comment_text = forms.CharField(widget=forms.Textarea)
