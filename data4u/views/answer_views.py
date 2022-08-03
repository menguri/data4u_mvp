from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Question_4, Answer
from ..forms import QuestionForm, AnswerForm

# Create your views here.abs()



@login_required(login_url='accounts:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question_4, pk=question_id)
    if request.user == question.author:
        messages.error(request, '자신의 질문엔 투표할 수 없습니다.')
        return redirect('data4u:detail', question_id=question_id)
    
    if request.method == 'POST':
        if question.answer_set.filter(author=request.user.id) :
            messages.error(request, '한번만 답변할 수 있습니다.')
            return redirect('data4u:detail', question_id=question_id)
        form = AnswerForm(request.POST)
        if form.is_valid():
        	answer = form.save(commit=False)
        	answer.author = request.user
        	answer.create_date = timezone.now()
        	answer.question = question
        	answer.save()
        	return redirect('{}#answer_{}'.format(resolve_url('data4u:detail', question_id=answer.question.id), answer.id))
    else:
        return HttpResponseNotAllowed('Only POST is possible.')


@login_required(login_url='accounts:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('data4u:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()  # 수정일시 저장
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('data4u:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
        question = get_object_or_404(Question_4, pk=answer.question.id)
    context = {'answer' : answer, 'form' : form, 'question' : question}
    return render(request, 'data4u/answer_form.html', context)


@login_required(login_url='accounts:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('data4u:detail', question_id=answer.question.id)
    answer.delete()
    return redirect('data4u:detail', question_id=answer.question.id)


@login_required(login_url='accounts:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인의 답변엔 투표할 수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(resolve_url('data4u:detail', question_id=answer.question.id), answer.id))