from datetime import date

from common.regular_expressions import username
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from profiles import validation_helper as vh
from profiles.models import GENDER_CHOICES


def get_select_years(back_count=100, start_year_decrease=0):
    now_year = date.today().year - start_year_decrease
    years = []

    for n in range(0, back_count + 1):
        years.append(now_year - n)

    return years


class RegisterProfileForm(vh.ValidateUsernameMixin, forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())
    username = forms.CharField(label="Username", max_length=100, validators=[
        RegexValidator(
            regex='^{0}$'.format(username),
            message='Username must be alphanumeric without special characters',
        ),
    ])
    display_name = forms.CharField(label="Display name", max_length=100)
    birthday = forms.DateField(label="Birthday",
                               widget=forms.SelectDateWidget(attrs={"class": "datepicker", "placeholder": "mm/dd/YY"},
                                                             years=get_select_years(100, 0)))
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES, widget=forms.RadioSelect())
    avatar = forms.ImageField()

    def clean(self):

        if 'email' in self.cleaned_data:
            same_email = User.objects.filter(email=self.cleaned_data['email'])
            if len(same_email) > 0:
                self.add_error('email', 'User with that email already exist.')
        self.validate_username()
