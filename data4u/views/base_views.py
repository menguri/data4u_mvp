from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from ..models import Question_4, Answer
from ..forms import QuestionForm, AnswerForm

# Create your views here.


def index(request):
    page = request.GET.get('page', '1') 	# 페이지
    kw = request.GET.get('kw', '')			# 검색어
    question_list = Question_4.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content1__icontains=kw) |  # 내용1 검색
            Q(content2__icontains=kw) |  # 내용2 검색
            Q(content3__icontains=kw) |  # 내용3 검색
            Q(content4__icontains=kw) |  # 내용4 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw)   # 질문 글쓴이 검색
        ).distinct()
    
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list' : page_obj, 'page':page, 'kw':kw}
    return render(request, 'data4u/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question_4, pk=question_id)
    context = {'question':question}
    # 각 문항별 횟수
    count_list = []
    for i in range(1, 5):
        count_list.append(question.answer_set.filter(content=i).count())
    context = {'question':question, 'count_list':count_list}
    return render(request, 'data4u/question_detail.html', context)
