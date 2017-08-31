# Register your models here.


from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from common.regular_expressions import username

username_field = forms.RegexField(
    label='Username',
    regex='^{0}$'.format(username),
    help_text='No spaces or special characters. Used for @username. Example: @taylorswift13.',
    error_messages={"invalid": 'Username must be alphanumeric without special characters.'})


class CustomUserCreationForm(UserCreationForm):
    username = username_field


class CustomUserChangeForm(UserChangeForm):
    username = username_field


class MyUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
