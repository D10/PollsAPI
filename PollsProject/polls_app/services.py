from django.contrib.auth.models import User
from rest_framework.response import Response


def response_text(text):
    return Response({'response': text})


# Функция, которая берет ID из POST запроса и авторизует или создает юзера с ником anonymous-{ID}
def authenticate_user(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user_id = request.POST.get('user_id')
        if not user_id:
            return
        user, _ = User.objects.get_or_create(username=f'anonymous-{user_id}', defaults={'password': 'Te123456'})
    return user
