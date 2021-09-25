from django.contrib import admin

from .models import Polls, Questions, Variation, Answers


@admin.register(Polls)
class PollsAdmin(admin.ModelAdmin):
    model = Polls
    list_display = ('id', 'title', 'date_start', 'date_end')
    readonly_fields = ('date_start', )


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    model = Questions
    list_display = ('id', 'poll', 'text', 'type')


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    model = Variation
    list_display = ('id', 'variation', )


@admin.register(Answers)
class AnswerAdmin(admin.ModelAdmin):
    model = Answers
    list_display = ('id', 'user', 'poll', 'question')
