from rest_framework import serializers

from .models import Polls, Answers, Questions


class QuestionSerializer(serializers.ModelSerializer):

    poll = serializers.SlugRelatedField(slug_field='title', many=False, queryset=Polls.objects.all())
    variations = serializers.StringRelatedField(many=True)

    class Meta:
        model = Questions
        fields = ('id', 'poll', 'text', 'type', 'variations')


class PollsSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Polls
        fields = ('id', 'title', 'description', 'date_start', 'date_end', 'questions')


class PollsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Polls
        fields = ('id', 'title', 'description', 'date_start', 'date_end')
