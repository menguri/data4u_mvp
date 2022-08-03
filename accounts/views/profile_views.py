from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from accounts.models import Profile
from accounts.forms import UserForm, ProfileForm
from data4u.models import Question_4, Answer
# Create your views here.

@login_required(login_url='accounts:login')
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    question_list = Question_4.objects.filter(author=pk)
    question_count = question_list.count()
    page = request.GET.get('page', '1')
    paginator = Paginator(question_list, 5)
    page_obj = paginator.get_page(page)
    context = {'question_list':page_obj, 'question_count':question_count}
    return render(request, 'accounts/profile.html', context)

@login_required(login_url='accounts:login')
def profile_register(request, pk):
    if request.method == 'POST' :
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, '프로필이 등록되었습니다.')
            # profile 페이지 이동
            return redirect('accounts:profile', pk)
    else:
        form = ProfileForm()
    context = {'form' : form}
    return render(request, 'accounts/profile_form.html', context)


@login_required(login_url='accounts:login')
def profile_modify(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST' :
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, '프로필 정보가 수정되었습니다.')
            # profile 페이지 이동
            return redirect('accounts:profile', pk)
    else:
        form = ProfileForm(instance=profile)
    context = {'form' : form}
    return render(request, 'accounts/profile_form.html', context)

@login_required(login_url='accounts:login')
def point_charge(request, pk):
    return render(request, 'accounts/point_charge.html')