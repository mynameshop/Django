from django.test import TestCase
from .admin import CustomUserChangeForm, CustomUserCreationForm


class AdminUsernameTests(TestCase):
    def test_invalid_user_names(self):
        invalid_user_list = ['Oba.ma', 'Obama-', 'O)bama', 'Ob ma']
        for user in invalid_user_list:
            form_data = {'username': user, 'password': 'QU!dIMhUuBN9t%Ik', "date_joined": "2/2/2010"}
            form = CustomUserChangeForm(data=form_data, initial={"password": "0"})
            self.assertTrue(not form.is_valid(),  "CustomUserChangeForm is valid for user %s" % user)
            form_data = {'username': user, 'password1': 'QU!dIMhUuBN9t%Ik', 'password2': 'QU!dIMhUuBN9t%Ik'}
            form = CustomUserCreationForm(data=form_data)
            self.assertTrue(not form.is_valid(), "CustomUserCreationForm is  valid for user %s" % user)

    def test_valid_user_name(self):
        valid_user_list = ['Obama', 'HillaryClinton', 'riahana2535', 'Jonh15Doe']
        for user in valid_user_list:
            form_data = {'username': user, 'password': 'QU!dIMhUuBN9t%Ik', "date_joined": "2/2/2010"}
            form = CustomUserChangeForm(data=form_data, initial={"password": "0"})
            self.assertTrue(form.is_valid(), "CustomUserChangeForm is not valid for user %s" % user)
            form_data = {'username': user, 'password1': 'QU!dIMhUuBN9t%Ik', 'password2': 'QU!dIMhUuBN9t%Ik'}
            form = CustomUserCreationForm(data=form_data)
            self.assertTrue(form.is_valid(), "CustomUserCreationForm is not valid for user %s" % user)
