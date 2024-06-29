from celery import shared_task

from .utils import send_notification, weekly_mailing
from .models import Response


@shared_task
def celery_notify_create_response(pk):
    """
    Таска вызывает метод 'send_notification' и передает в него ряд параметров
    для формирования и отправки почтового уведомления.
    """
    instance = Response.objects.get(pk=pk)
    post = instance.post
    subscriber = post.user
    sender = instance.user
    mode = 'create'

    send_notification(instance.text, post.pk, post.category, post.title, subscriber, sender, mode)


@shared_task
def celery_notify_update_response(pk):
    """
    Таска вызывается только при нажатии кнопки "Accept/Decline" автором поста.
    Передает status для индикации действия "Accept/Decline".
    """
    instance = Response.objects.get(pk=pk)
    post = instance.post
    subscriber = instance.user
    sender = post.user  # другой sender
    mode = 'update'  # другой режим
    status = instance.accept

    send_notification(instance.text, post.pk, post.category, post.title, subscriber, sender, mode, status)


@shared_task
def celery_notify_delete_response(pk):
    """
    Таска вызывается при удалении комментария автором поста;
    автор комментария получит на почту письмо с уведомлением.
    """
    instance = Response.objects.get(pk=pk)
    post = instance.post
    subscriber = instance.user
    sender = post.user
    mode = 'delete'

    send_notification(instance.text, post.pk, post.category, post.title, subscriber, sender, mode)


@shared_task
def celery_weekly_mailing():
    """
    Таска еженедельной рассылки;
    функцию рассылки импортируем из утилит.

    upd: возможность отправлять пользователям новостные рассылки.
    """
    weekly_mailing()