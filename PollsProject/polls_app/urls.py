from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

polls_list = views.PollsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
polls_detail = views.PollsViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})
answer = views.PollsViewSet.as_view({
    'get': 'get_user_questions',
    'post': 'get_user_questions'
})
post_answer = views.PollsViewSet.as_view({
    'post': 'answer_the_question'
})
questions_list = views.QuestionsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
questions_detail = views.QuestionsViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})
my_answers = views.PollsViewSet.as_view({
    'post': 'get_user_answers'
})

urlpatterns = format_suffix_patterns([
    path('polls/', polls_list, name='polls-list'),
    path('polls/<int:pk>', polls_detail, name='polls-detail'),
    path('polls/<int:pk>/answer/', answer, name='take-a-poll'),
    path('polls/<int:pk>/answer/<int:ans_pk>', post_answer, name='answer-the-question'),
    path('questions/', questions_list, name='questions-list'),
    path('questions/<int:pk>', questions_detail, name='questions-detail'),
    path('my_answers/', my_answers, name='my_answers')
])
