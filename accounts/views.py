from django.shortcuts import render,redirect
from .forms import CustomSignupForm
from allauth.account.views import SignupView,LoginView
from allauth.account.forms import LoginForm
from django.urls import reverse_lazy,reverse
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation

# Create your views here.
class CustomAllAuthLoginView(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('home'))  # Redirect to home page if user is authenticated
        return super().get(request, *args, **kwargs)


class CustomSignUpView(SignupView):
    form_class = CustomSignupForm

    def form_valid(self, form):
        # Create the user but don't log them in
        self.user = form.save(self.request)
        return redirect("account_email_verification_sent")  # Redirect to the login page

    # Optional: Override the success url to redirect after email confirmation
    def get_success_url(self):
        return reverse("account_email_verification_sent")  # Redirect to the login page
        

def send_verification_email(request, user):
    email_address = EmailAddress.objects.get(user=user, primary=True)
    send_email_confirmation(request, email_address)