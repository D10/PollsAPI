import datetime

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Polls, Questions, Variation, Answers
from .serializers import PollsSerializer, PollsListSerializer, QuestionSerializer
from .services import response_text, authenticate_user


class PollsViewSet(viewsets.ModelViewSet):

    """Основной класс, который реализует весь функционал получения опросов,
    их прохождения и получения пройденых опросов"""

    serializer_class = PollsSerializer
    queryset = Polls.objects.filter(date_end__gt=datetime.date.today())

    # Распределяем классы сериализации, чтобы при выводе списка Опросов выводить только основную информацию
    def get_serializer_class(self):
        if self.action == 'list':
            return PollsListSerializer
        else:
            return PollsSerializer

    # Распределяем доступы между пользователем и админом
    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'get_user_questions',
                           'answer_the_question', 'get_user_answers'):
            permission_classes = [permissions.AllowAny, ]
        else:
            permission_classes = [permissions.IsAdminUser, ]
        return [permission() for permission in permission_classes]

    # Достаем из POST запроса ответы на вопрос и возвращаем кверисеты
    def get_answers(self):
        answers = self.request.POST.get('answers')
        if answers:
            answers = [Variation.objects.get(variation=i) for i in answers.split(', ')]
            return answers
        return

    # Выводим из опроса список вопросов, на которые еще не ответил юзер
    @action(detail=True, methods=['post', ], permission_classes=[permissions.AllowAny, ])
    def get_user_questions(self, *args, **kwargs):
        user = authenticate_user(self.request)
        if not user:
            return response_text('UID пользователя не был передан')
        poll = self.get_object()
        queryset = Questions.objects.filter(poll=poll).exclude(answer__user=user)
        if not queryset:
            return response_text('Вы уже прошли этот опрос')
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)

    # Принимаем ответ на вопрос из api/{pk}/answer/{pk}, проводим валидацию и сохраняем его
    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.AllowAny, ])
    def answer_the_question(self, *args, **kwargs):
        user = authenticate_user(self.request)
        if not user:
            return response_text('UID пользователя не был передан')
        question_id = self.kwargs['ans_pk']
        poll_id = self.kwargs['pk']
        answers = self.get_answers()
        question = Questions.objects.get(pk=question_id)
        if question.type == 'text':
            answer_text = self.request.POST.get('answer_text')
            if not answer_text:
                return response_text('Вы не ввели текст ответа!')
            Answers(user=user, poll_id=poll_id,
                    question_id=question_id, answer_text=answer_text).save()
        else:
            if not answers:
                return response_text('Выберите один из вариантов ответа!')
            if question.type == 'variation' and len(answers) > 1:
                return response_text('В данном вопросе допустим только один вариант ответа!')
            user_answer = Answers.objects.create(user=user, poll_id=poll_id, question_id=question_id)
            user_answer.answers.add(*answers)
        return response_text('Ваш ответ принят')

    @action(detail=False, methods=['post', ], permissions_classes=[permissions.AllowAny, ])
    def get_user_answers(self, *args, **kwargs):
        user = authenticate_user(self.request)
        if not user:
            return response_text('UID пользователя не был передан')
        user_polls = Polls.objects.filter(answers__user=user).distinct()
        if not user_polls:
            return response_text('У Вас пока нет пройденых опросов')
        result = []
        for poll in user_polls:
            print(poll)
            if Answers.objects.filter(user=user, poll=poll).count() == Answers.objects.filter(poll=poll).count():
                user_poll = dict()
                user_poll['id'] = poll.pk
                user_poll['title'] = poll.title
                user_poll['answers'] = list()
                for answer in Answers.objects.filter(poll=poll, user=user):
                    answers_dict = dict()
                    answers_dict['id'] = answer.id
                    answers_dict['question'] = answer.question.text
                    answers_dict['answers'] = answer.answers.all().values_list('variation', flat=True)
                    answers_dict['answers_text'] = answer.answer_text
                    user_poll['answers'].append(answers_dict)
                result.append(user_poll)
        return Response(result)


class QuestionsViewSet(viewsets.ModelViewSet):

    # Класс для просмотра/создания/изменения/удаления вопросов админом

    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
