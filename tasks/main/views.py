from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django_otp.decorators import otp_required
from .forms import EmailForm
from .tasks import send_email_task


def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save()
            send_email_task.delay(email.recipient, email.subject, email.body)
            messages.success(request, 'Your email is being sent in the background!')
            return redirect('send_email')
    else:
        form = EmailForm()
    return render(request, 'send_email.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


@otp_required
def protected_view(request):
    return render(request, "protected.html")