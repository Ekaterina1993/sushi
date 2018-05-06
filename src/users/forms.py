from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

User = get_user_model()


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'old_password',
            'new_password1',
            'new_password2')
        self.helper.add_input(Submit('submit', 'Submit'))


class LoginForm(auth_forms.AuthenticationForm):
    username = forms.EmailField(label=_('Email'), max_length=30)
    remember_me = forms.BooleanField(
        label=_('Remember me'), required=False, initial=True)

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(request, *args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('username', id='login_username'),
            Field('password', id='login_password'),
            Field('remember_me',),
        )
        self.helper.add_input(Submit('submit', 'Login'))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,
                               label=_('Create Password'))
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_('Confirm Password'))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            'password',
            'password1')
        self.helper.add_input(Submit('submit', 'Register'))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email):
            raise forms.ValidationError(
                _("This email is already taken, chose an another one please."))
        return email

    def clean(self):
        if 'password' in self.cleaned_data and 'password1' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password1']:
                raise forms.ValidationError(
                    _("The two password fields didn't match."))

        self.cleaned_data['last_login'] = datetime.now()

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['email', 'password', ]


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'avatar']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'avatar')
        self.helper.add_input(Submit('submit', 'Update'))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk):
            raise forms.ValidationError(
                _("This email is already taken, chose an another one please."))
        return email
