from django.contrib.auth.models import User
from django.db import models


class Polls(models.Model):
    title = models.CharField(verbose_name='Название', max_length=167)
    description = models.TextField(verbose_name='Описание')
    date_start = models.DateField(verbose_name='Дата старта', auto_now_add=True, editable=False)
    date_end = models.DateField(verbose_name='Дата окончания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Questions(models.Model):
    TEXT = 'text'
    VARIATION = 'variation'
    VARIATIONS = 'variations'

    CHOICES = (
        (TEXT, 'Текстом'),
        (VARIATION, 'Один вариант'),
        (VARIATIONS, 'Несколько вариантов')
    )

    poll = models.ForeignKey(Polls,  verbose_name='Опрос', on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name='Текст вопроса')
    type = models.CharField(verbose_name='Тип вопроса', choices=CHOICES, max_length=20)
    variations = models.ManyToManyField('Variation', verbose_name='Варианты', blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Variation(models.Model):
    variation = models.TextField(verbose_name='Текст ответа')

    def __str__(self):
        return self.variation

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'


class Answers(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    poll = models.ForeignKey(Polls, verbose_name='Опрос', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Questions, verbose_name='Вопрос', on_delete=models.CASCADE, related_name='answer')
    answer_text = models.TextField(verbose_name='Ответ текстом', blank=True, null=True)
    answers = models.ManyToManyField(Variation, verbose_name='Ответы', blank=True)

    def __str__(self):
        return f'Ответ из опроса {self.poll.title} от {self.user.username}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
