from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, GuestForm
from django.utils.http import is_safe_url
from .models import GuestModel
from django.views.generic import CreateView, FormView

# Create your views here.
def guest_register_page(request):
    form = GuestForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        email = form.cleaned_data.get("email")
        next_ = request.GET.get('next_url')
        next_post = request.POST.get('next_url')
        redirect_path = next_ or next_post or None
        if email is not None:
            new_guest_email = GuestModel.objects.create(email=email)
            request.session['guest_email_id'] = new_guest_email.id
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
    return redirect("/register/")

class LoginView(FormView):
    template_name = 'auth/login_page.html'
    success_url = '/'
    form_class = LoginForm
    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        next_ = request.GET.get('next_url')
        next_post = request.POST.get('next_url')
        redirect_path = next_ or next_post or None
        user = authenticate(username=email, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            try:
                # after login, no more guest user
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            return redirect("/")
        return super(LoginView, self).form_invalid()

# Create your views here.
# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form":form
#     }
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(username=username, password=password)
#         next_ = request.GET.get('next_url')
#         next_post = request.POST.get('next_url')
#         redirect_path = next_ or next_post or None
#         if user is not None:
#             # A backend authenticated the credentials
#             login(request, user)
#             try:
#                 # after login, no more guest user
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             return redirect("/")
#         else:
#             # No backend authenticated the credentials
#             print("No such user")
#         form = LoginForm()
#     return render(request,"auth/login_page.html",context)

class RegisterView(CreateView):
    template_name = 'auth/register_page.html'
    form_class = RegisterForm
    success_url = '/login'