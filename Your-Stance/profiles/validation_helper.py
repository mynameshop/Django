from django.contrib.auth.models import User

class ValidateUsernameMixin(object):
    def validate_username(self, user_instance=None):
        if 'username' in self.cleaned_data:
            same_username = User.objects.filter(username__iexact=self.cleaned_data['username']).first()
            if same_username is not None and\
                same_username.pk is not None and \
                user_instance != same_username: 
                    self.add_error('username', 'User with such username already exist.')