from django.shortcuts import render, redirect
from django.contrib import messages
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
