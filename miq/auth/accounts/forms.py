
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Mixin(object):
    def clean_username(self):
        return self.cleaned_data.get('username').lower()


"""
SIGN UP
"""


class SignupForm(Mixin, auth_forms.UserCreationForm):

    username = forms.CharField(min_length=4)

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'password1', 'password2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

        self.fields["email"].help_text = _(
            'We will send you a verification email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('This user already exists.'))
        return email


"""
SIGN IN
"""


class AuthenticationForm(Mixin, auth_forms.AuthenticationForm):
    pass
