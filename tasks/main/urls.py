from django.urls import path
from .views import send_email_view, register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('send-email/', send_email_view, name='send_email'),
    path("register/", register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]