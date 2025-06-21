from django.shortcuts import render, redirect


def main(request):
    return render(request, 'index.html')


def error(response, message):
    return render(
        response,
        'error.html',
        {
            'message': message
        }
    )

# ------------------------------------------------------------------------
# лише на час розробки потім прибрати - це мій ІД
from django.contrib.auth import login
from django.contrib.auth import get_user_model


User = get_user_model()
ID = 4


def dev_login(request):
    if not request.user.is_authenticated:
        dev_user = User.objects.get(username="viktor")  # або твій логін
        dev_user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, dev_user)
    return redirect('note_app:note-main')
# ------------------------------------------------------------------------
