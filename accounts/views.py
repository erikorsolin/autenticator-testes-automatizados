from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'accounts/home.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Credenciais inválidas")
    
    return render(request, 'accounts/login.html')


def user_register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                messages.error(request, "Usuário já existe")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email já cadastrado")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, "Cadastro realizado com sucesso! Faça login.")
                return redirect('login')
        else:
            messages.error(request, "As senhas não coincidem")

    return render(request, 'accounts/register.html')


def user_logout(request):
    logout(request)
    messages.success(request, "Você saiu com sucesso")
    return redirect('home')


def forget_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                from_email="noreply@seusite.com",
                email_template_name="accounts/password_reset_email.html",
            )
            messages.success(request, "Email de recuperação enviado!")
            return redirect('login')
    else:
        form = PasswordResetForm()

    return render(request, 'accounts/forget_password.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})
