from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Question_4, Answer
from ..forms import QuestionForm, AnswerForm
from accounts.models import Profile
# Create your views here.


@login_required(login_url='accounts:login')
def question_create(request):
    try:
        profile = get_object_or_404(Profile, user=request.user)
        if profile.point >= 1000:
            pass
        else:
            messages.error(request, '포인트를 충전해주세요.')
            return redirect('accounts:profile', request.user.id)
    except:
        messages.error(request, '프로필을 먼저 등록해주세요.')
        return redirect('accounts:profile', request.user.id)
    
    if request.method == 'POST' :
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            
            # 포인트 차감 -1000
            profile.point -= 1000
            profile.save()
            
            return redirect('data4u:index')
    else:
    	form = QuestionForm(initial={'subject': '제목을 입력하세요.', 'content1':'1번 선택지', 'content2':'2번 선택지', 'content3':'3번 선택지', 'content4':'4번 선택지'})
    context = {'form':form}
    return render(request, 'data4u/question_form.html', context)


@login_required(login_url='accounts:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question_4, pk=question_id)
    if request.user != question.author :
        messages.error(request, '수정권한이 없습니다.')
        return redirect('data4u:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('data4u:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form' : form}
    return render(request, 'data4u/question_form.html', context)


@login_required(login_url='accounts:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question_4, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('data4u:detail', question_id=question.id)
    question.delete()
    return redirect('data4u:index')


@login_required(login_url='accounts:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question_4, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인 질문에는 투표할 수 없습니다.')
    else:
        question.voter.add(request.user)
    return redirect('data4u:detail', question_id=question.id)