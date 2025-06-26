from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from .forms import RegisterForm, LoginForm


def send_activation_email(request, user):
    # Генерація токена та UID
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Посилання для активації
    activation_link = f"{request.scheme}://{request.get_host()}/users/activate/{uid}/{token}/"

    # Відправка email
    subject = "Activate your account"
    message = render_to_string("users/activation_email.html", {
        'user': user.username,
        'activation_link': activation_link
    })
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
        headers={'Reply-To': 'noreply@meta.ua'}
    )
    email.content_subtype = "html"
    email.send()


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(request, user)
            # return redirect(to='main')
            return redirect('users:signup-success')
        else:
            # не валідна форма - повертаємося до реєстрації
            # print(":x: Signup Form Errors:", form.errors)
            return render(request, 'users/signup.html', context={"form": form})

    return render(
        request,
        'users/signup.html',
        context={"form": RegisterForm()}
    )


def signup_success(request):
    return render(request, 'users/signup_success.html')


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='basic_project:main')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is None:
                messages.error(request, 'Username or password didn\'t match')
                return redirect(to='users:login')
            login(request, user)
            return redirect(to='main')
        else:
            print(form.errors)
    return render(request, 'users/login.html', context={"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='main')


def activate_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now login.')
        return redirect('users:login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('users:signup')
