from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import RegisterUserForm, InteriorDesignRequestForm
from .models import AdvUser, InteriorDesignRequest
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib import messages

def index(request):
    requests = InteriorDesignRequest.objects.all()
    if not request.user.is_authenticated:
        requests = []
    return render(request, 'catalog/index.html', {'requests': requests})

def profile(request):
    user_requests = InteriorDesignRequest.objects.filter(user=request.user)
    return render(request, 'catalog/profile.html', {'user_requests': user_requests})

class login(LoginView):
    template_name = 'catalog/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.warning(self.request, "Ваш аккаунт не активирован. Ожидайте активации от администратора.")
            return self.get(form)

        response = super().form_valid(form)
        user.status = 'online'
        user.save()
        if 'registration_message' in self.request.session:
            messages.success(self.request, self.request.session['registration_message'])
            del self.request.session['registration_message']
        return response

class logout(LoginRequiredMixin, LogoutView):
    template_name = 'catalog/logout.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'catalog/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('catalog:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.is_activated = False
        user.save()

        self.request.session['registration_message'] = 'Вы успешно зарегистрированы! Ожидайте активации от администратора.'

        return super().form_valid(form)

class RegisterDoneView(TemplateView):
    template_name = 'catalog/register_done.html'

def activate_user(request, user_id):
    user = get_object_or_404(AdvUser, id=user_id)
    user.is_activated = True
    user.is_active = True
    user.save()
    messages.success(request, f'Пользователь {user.username} успешно активирован!')
    return redirect('admin:index')

def create_request(request):
    if request.user.is_staff:
        messages.error(request, "Администраторы не могут создавать заявки.")
        return redirect('catalog:profile')

    if not request.user.is_active:
        messages.error(request, "Вы не можете создавать заявки до активации.")
        return redirect('catalog:profile')

    if not request.user.is_active:
        messages.error(request, "Вы не можете создавать заявки до активации.")
        return redirect('catalog:profile')

    if request.method == 'POST':
        form = InteriorDesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user
            request_instance.category = form.cleaned_data['new_category'] or form.cleaned_data['category']
            request_instance.save()
            messages.success(request, 'Ваша заявка успешно отправлена!')
            return redirect('catalog:profile')
    else:
        form = InteriorDesignRequestForm()

    return render(request, 'catalog/create_requests.html', {'form': form})

def delete_request(request):
    user_requests = InteriorDesignRequest.objects.filter(user=request.user)
    if request.user.is_staff:
        messages.error(request, "Администраторы не могут удалять заявки.")
        return redirect('catalog:profile')

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        request_instance = get_object_or_404(InteriorDesignRequest, id=request_id, user=request.user)
        request_instance.delete()
        messages.success(request, "Заявка успешно удалена.")
        return redirect('catalog:profile')

    return render(request, 'catalog/delete_request.html', {'user_requests': user_requests})