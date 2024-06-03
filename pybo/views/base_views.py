from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from ..models import Question, Answer ,Comment


def index(request, category_id=1):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준
    if category_id <= 2:
        # 기본 카테고리 필터링
        question_list = Question.objects.filter(category=category_id)

        # 정렬
        if so == 'recommend':
            question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
        elif so == 'popular':
            question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
        else:  # recent
            question_list = question_list.order_by('-create_date')

        # 검색
        if kw:
            question_list = question_list.filter(
                Q(subject__icontains=kw) |  # 제목검색
                Q(content__icontains=kw) |  # 내용검색
                Q(author__username__icontains=kw) |  # 질문 글쓴이검색
                Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
            ).distinct()
    elif category_id == 3:
        question_list = Answer.objects.all().order_by('-create_date')
    else:
        question_list = Comment.objects.all().order_by('-create_date')

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so, 'category_id': category_id}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)