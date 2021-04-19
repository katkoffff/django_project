from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Replay


@receiver(post_save, sender=Replay)
def notify_created_replay(sender, instance, created, **kwargs):
    if created:
        replay = Replay.objects.get(pk=instance.id)
        post_head = replay.post.head
        post_author = replay.post.author.user
        post_author_email = post_author.email
        replay_author = replay.author.user
        try:
            send_mail(
                subject=f'new_replay',
                message=f"На вашу статью {post_head} написал отклик {replay_author}",
                from_email='katkofff@yandex.ru',
                recipient_list=[f'{post_author_email}', ]
            )
            print(f'send email to {post_author_email}')
        except Exception:
            print('spam')
    else:
        replay = Replay.objects.get(pk=instance.id)
        if replay.status == 'CF':
            replay_post_head = replay.post.head
            replay_author = replay.post.author.user
            replay_author_email = replay.author.user.email
            try:
                send_mail(
                    subject=f'new_replay',
                    message=f"Ваш отклик на статью {replay_post_head} был принят автором {replay_author}",
                    from_email='katkofff@yandex.ru',
                    recipient_list=[f'{replay_author_email}', ]
                )
                print(f'send email to {replay_author_email}')
            except Exception:
                print('spam')
        elif replay.status == 'RJ':
            replay_post_head = replay.post.head
            replay_author = replay.post.author.user
            replay_author_email = replay.author.user.email
            try:
                send_mail(
                    subject=f'new_replay',
                    message=f"Ваш отклик на статью {replay_post_head} был отклонен автором {replay_author}",
                    from_email='katkofff@yandex.ru',
                    recipient_list=[f'{replay_author_email}', ]
                )
                print(f'send email to {replay_author_email}')
            except Exception:
                print('spam')


