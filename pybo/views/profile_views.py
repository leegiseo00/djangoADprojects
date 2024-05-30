from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from ..models import User, Question, Answer, Comment, Profile

def profile_introduction(request, username):
    profile_user = get_object_or_404(User, username=username)

    profile = Profile.objects.get(author=profile_user)

    context = {'profile_user': profile_user, 'introduction': profile.introduction}

    return render(request, 'pybo/profile_introduction.html', context)


def profile_question(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 기본 카테고리 필터링
    question_list = Question.objects.filter(author=profile_user)

    # 정렬
    if so == 'recommend':
        question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = question_list.order_by('-create_date')

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'profile_user': profile_user, 'question_list': page_obj, 'page': page, 'so': so}
    return render(request, 'pybo/profile_question.html', context)


def profile_answer(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 기본 카테고리 필터링
    answer_list = Answer.objects.filter(author=profile_user)

    # 정렬
    if so == 'recommend':
        answer_list = answer_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        answer_list = answer_list.annotate(num_answer=Count('question__answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        answer_list = answer_list.order_by('-create_date')

    # 페이징처리
    paginator = Paginator(answer_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'profile_user': profile_user, 'answer_list': page_obj, 'page': page, 'so': so}
    return render(request, 'pybo/profile_answer.html', context)


def profile_comment(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 기본 카테고리 필터링
    comment_list = Comment.objects.filter(author=profile_user)

    # 정렬
    if so == 'popular':
        comment_list = comment_list.annotate(num_answer=Count('question__answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        comment_list = comment_list.order_by('-create_date')

    # 페이징처리
    paginator = Paginator(comment_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'profile_user': profile_user, 'comment_list': page_obj, 'page': page, 'so': so}
    return render(request, 'pybo/profile_comment.html', context)