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
from django.contrib.auth import authenticate, login as auth_login

def index(request):
    requests = InteriorDesignRequest.objects.all()
    return render(request, 'catalog/index.html', {'requests': requests})

@login_required
def profile(request):
    user_requests = InteriorDesignRequest.objects.filter(user=request.user)
    return render(request, 'catalog/profile.html', {'user_requests': user_requests})

class login(LoginView):
    template_name = 'catalog/login.html'

class logout(LoginRequiredMixin, LogoutView):
    template_name = 'catalog/logout.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'catalog/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('catalog:register_done')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.is_activated = False
        user.has_logged_in = False
        user.save()

        messages.success(self.request, 'Вы успешно зарегистрированы! Ожидайте активации от администратора.')

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


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            user.has_logged_in = True
            user.save()
            return redirect('catalog/index')

    return render(request, 'login.html')

def create_request(request):
    if request.method == 'POST':
        form = InteriorDesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user
            request_instance.save()
            messages.success(request, 'Ваша заявка успешно отправлена!')
            return redirect('catalog:profile')
    else:
        form = InteriorDesignRequestForm()

    return render(request, 'catalog/create_requests.html', {'form': form})