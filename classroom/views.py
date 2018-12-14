from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm
from django.views.generic import CreateView, FormView
from django.utils.http import is_safe_url
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('register')
    template_name = 'login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)


def PostView(request):
    if request.method == 'POST':
        title = request.POST["title"]
        body = request.POST["body"]
        email = request.POST["email"]
        password = request.POST["password"]
        author = User(email=email, password=password)
        p = Profile(author=author,title=title,body=body)
        p.save()
        return render(request,"classroom/post.html")