from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .tasks import celery_notify_create_response, celery_notify_update_response, celery_notify_delete_response
from .models import Response


@receiver(post_save, sender=Response)  # Comment --> Post (1)
def notify_about_save_response(sender, instance, **kwargs):  # instance : объект статьи
    """
    Сигнал срабатывает при создании/редактировании комментария к посту
    и вызывает соответсвующую таску из mailing.tasks;
    метод 'delay' передает не объект, но только id экземпляра.

    :param instance: экземпляр модели Comment
    """
    # Comment --> Post
    if kwargs['created']:  # kwargs['created'] == True
        celery_notify_create_response.delay(instance.pk)
    # Accept/Decline --> Comment
    elif kwargs['update_fields']:
        celery_notify_update_response.delay(instance.pk)


# Delete --> Comment
@receiver(pre_delete, sender=Response)
def notify_about_delete_response(sender, instance, **kwargs):
    """
    Сигнал срабатывает вначале удаление экземпляра модели Comment;
    в вызываемую таску передается полностью удаляемый объект.
    """
    celery_notify_delete_response(instance.pk)