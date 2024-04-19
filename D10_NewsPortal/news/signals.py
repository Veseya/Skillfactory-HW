from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .task import send_email_task


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        send_email_task.delay(instance.pk)

