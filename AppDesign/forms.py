from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import AdvUser, InteriorDesignRequest, Category
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

class InteriorDesignRequestForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100, required=False, label="Категория")
    is_urgent = forms.BooleanField(required=False, label='Срочность')

    class Meta:
        model = InteriorDesignRequest
        fields = ['name','email', 'phone', 'project_description', 'design_image', 'new_category', 'is_urgent']
        widgets = {
            'project_description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_new_category(self):
        category_name = self.cleaned_data.get('new_category')
        if category_name:
            category, created = Category.objects.get_or_create(name=category_name)
            return category
        return None

    def clean_design_image(self):
        image = self.cleaned_data.get('design_image')
        if image:
            if image.size > 2 * 1024 * 1024:  # 2 MB
                raise ValidationError('Размер изображения не должен превышать 2 Мб.')
            if not image.name.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                raise ValidationError('Неподдерживаемый формат файла. Используйте jpg, jpeg, png или bmp.')
            return image
        raise forms.ValidationError("Необходимо загрузить изображение.")