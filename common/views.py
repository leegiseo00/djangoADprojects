from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from pybo.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import ProfileForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='common/password_reset_email.html',
                subject_template_name='common/password_reset_subject.txt',
            )
            return redirect('common:login')
    else:
        form = PasswordResetForm()

    context = {
        'form': form
    }
    return render(request, 'common/password_reset.html', context)


@login_required
def account_settings(request):
    profile, _ = Profile.objects.get_or_create(author=request.user)

    if request.method == 'POST':
        if 'password_submit' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, '비밀번호가 성공적으로 업데이트되었습니다.')
                return redirect('common:account_settings')
        elif 'profile_submit' in request.POST:
            profile_form = ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, '자기소개가 성공적으로 업데이트되었습니다.')
                return redirect('common:account_settings')
    else:
        password_form = PasswordChangeForm(request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'common/account_settings.html', {'password_form': password_form, 'profile_form': profile_form})


def logout_view(request):
    logout(request)
    return redirect('index')


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


# User 모델 인스턴스가 저장된 후에 실행될 함수
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(author=instance)

# User 모델 인스턴스가 저장될 때마다 실행될 함수
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()