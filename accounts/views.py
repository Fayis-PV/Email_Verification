from django.shortcuts import render,redirect
from .forms import CustomSignupForm
from allauth.account.views import SignupView,LoginView
from allauth.account.forms import LoginForm
from django.urls import reverse_lazy,reverse
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import get_user_model
from allauth.account.views import EmailVerificationSentView,ConfirmEmailView
from django.shortcuts import get_object_or_404


User = get_user_model()

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
        
        # Redirect with user ID as query parameter
        verification_url = reverse('account_email_verification_sent')
        verification_url += f'?id={self.user.id}&verify=True'
        return redirect(verification_url)

    # Optional: Override the success url to redirect after email confirmation
    def get_success_url(self):
        return reverse("account_email_verification_sent")  # Redirect to the login page
        

class CustomEmailVerificationSentView(EmailVerificationSentView):
    template_name = 'account/verification_sent.html'

    def send_verification_email(self, request, user):
        email_address = EmailAddress.objects.get(user=user, primary=True)
        send_email_confirmation(request, user=user, email=email_address)
        return user.id


    def get(self, request, *args, **kwargs):
        if self.request.GET.get('id'):
            user_id = self.request.GET.get('id')
            user = get_object_or_404(User, id=user_id)
            if 'verify' in request.GET:
                user_id = self.send_verification_email(request, user)
                redirect_url = reverse('account_email_verification_sent') + f'?id={user_id}'
                return redirect(redirect_url)
            return self.render_to_response(self.get_context_data(user=user))
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user_email = request.POST.get('email')  # Retrieve the user's email
        print(user_email)
        user = get_object_or_404(User, email=user_email)
        
        user_id = self.send_verification_email(request, user)
        redirect_url = reverse('account_email_verification_sent') + f'?id={user_id}'
        return redirect(redirect_url)
    

class CustomConfirmEmailView(ConfirmEmailView):
    def get(self,*args, **kwargs):
        if self.request.user:
        
            return redirect('account_login')
        
        super().get(self,*args, **kwargs)
            
