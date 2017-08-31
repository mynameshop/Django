# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from .fields import CreditCardField, CreditCardExpiryField, CreditCardCVV2Field

class CreditcardForm(forms.Form):
    acct = CreditCardField(label='Card Number')
    expdate = CreditCardExpiryField(label='Expiration Date')
    cvv2 = CreditCardCVV2Field(label='CVV2', )
    stripe_token = forms.CharField(required=True, widget=forms.HiddenInput)
     
    class Media:
        js = {
            'https://js.stripe.com/v2/'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['acct'].widget.attrs['class'] = 'form-control'
        self.fields['expdate'].widget.attrs['class'] = 'form-control form-control-expdate'
        self.fields['cvv2'].widget.attrs['class'] = 'form-control'

    def clean_acct(self):
        acct = self.cleaned_data.get('acct')
        if not self.fields['acct'].required:
            return acct
        if acct is None or len(acct) == 0:
            raise forms.ValidationError('This field is required.')
        return acct
