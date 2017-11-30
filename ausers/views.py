from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from .forms import UserForm
from .models import User


class RegisterView(CreateView):
    form_class = UserForm
    template_name = 'register.html'
    success_url = '/profile'

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        if not self.request.user.is_anonymous():
            self.template_name = 'profile.html'
            context['user'] = self.request.user
        return context

    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password')
        user = User.objects.get(email=email, password=password)
        login(self.request, user)
        return valid


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        if self.request.user.is_anonymous():
            return redirect('/')
        context['user'] = self.request.user
        return context


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        if not self.request.user.is_anonymous():
            self.template_name = 'profile.html'
            context['user'] = self.request.user
        return context


def logout_view(request):
    logout(request)
    return redirect('index')

def auth_user_try(request):
    try:
        user = User.objects.get(email=request.POST['email'], password=request.POST['password'])
    except User.DoesNotExist:
        return redirect('index')
    login(request, user)
    return redirect('profile')
