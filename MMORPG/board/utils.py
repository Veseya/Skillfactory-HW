import datetime

from django.conf import settings  # LazySettings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, User


def response_not_in_user_post(request, response):
    """
    Метод проверяет, входит ли пост, к которому принадлежит переданный комментарий,
    во множество всех постов, принадлежащих автору.
    """
    response_post = response.post
    user_posts = Post.objects.filter(user=request.user)
    return response_post not in user_posts

def send_notification(text, pk, category, title, subscriber, sender, mode='create', status=None):
    """
    Функция формирует контекст для почтового шаблона, на основе полученных
    из таски параметров создаёт письмо, прикрепляет к нему
    контент [шаблон + контекст] и отправляет адресату.

    :param text: текст комментария
    :param pk: id связанного* поста
    :param category: категория поста*
    :param title: заголовок поста*
    :param subscriber: автор поста*
    :param sender: автор комментария
    :param mode: задаёт шаблон и тему письма
    :param status: статус отклика (принят/отклонен)
    """

    if mode == 'create':
        template = 'response_created_email'
        subject = f'Reply to "{title}"'
    elif mode == 'update':
        template = 'response_updated_email'
        status = 'status' if status else 'declined'
        subject = f'{sender} has {status} your response'
    elif mode == 'delete':
        template = 'response_delete_email'
        subject = f'{sender} has deleted your response'

    html_content = render_to_string(
        # template changes depending on the mode
        f'mailing/{template}.html',
        {
            'text': text,
            'link': f'{settings.SITE_URL}/board/{pk}',
            'username': subscriber.username,
            'category': category,
            'sender': sender,
        }
    )

    # время отправки без микросекунд для заголовка [тестирование отправки]
    # sending_time = datetime.datetime.now().replace(microsecond=0)

    msg = EmailMultiAlternatives(
        # subject changes depending on the mode
        subject=f'{subject}',
        body='',  # body задаем выше в html_content
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[subscriber.email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def weekly_mailing():
    """
    Функция еженедельной расслыки;
    рассылает всем пользователям перечень постов за последние 7 дней.
    """
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(pub_date__gte=last_week)  # lookup __gte
    subscribers = set(User.objects.values_list('email', flat=True))

    html_content = render_to_string(
        'mailing/weekly_news.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    sending_time = datetime.datetime.now().replace(microsecond=0)

    msg = EmailMultiAlternatives(
        subject=f'Post from last week [{sending_time}]',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=subscribers  # bcc скрывает адреса в массовой рассылке
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print(f'msg sent {sending_time}')