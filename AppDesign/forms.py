from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import AdvUser
from .validators import validate_cyrillic

from .models import user_registrated

class RegisterUserForm(forms.ModelForm):
    full_name = forms.CharField(
        required=True,
        label='Ф.И.О.',
        validators=[validate_cyrillic],
        widget=forms.TextInput()
    )
    login = forms.CharField(required=True, widget=forms.TextInput(), label="Ваш логин")
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput, help_text='Повторите тот же самый пароль еще раз')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_activated = True
        user.login = self.cleaned_data['login']
        user.full_name = self.cleaned_data['full_name']
        if commit:
            user.save()
            user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('full_name','login', 'email', 'password1', 'password2', 'send_messages')

