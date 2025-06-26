from django.shortcuts import render, redirect


def main(request):
    return render(request, 'index.html')


def error(request, message, status=404):
    return render(
        request,
        'error.html',
        {
            'message': message
        },
        status=status,
    )


def custom_404(request, exception):
    return error(request, "⛔ Page not found (404)")


def custom_500(request):
    return error("💥 Server error (500)")
