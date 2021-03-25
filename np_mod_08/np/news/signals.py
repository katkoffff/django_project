from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post, PostCategory, Category, CategorySubscribers
from django.contrib.auth.models import User
import time


@receiver(post_save, sender=Post)
def notify_managers_created_post(sender, instance, created, **kwargs):
    if created:
        subject = f'Вышла новая стать по теме на которую вы подписаны'
        print('created')
        print(instance.id)
        cat_id = PostCategory.objects.filter(to_posts_id=instance.id-1).values('to_categorys_id')
        print(cat_id)
        for c_id in cat_id:
            use_id = CategorySubscribers.objects.filter(category__id=c_id['to_categorys_id']).values('user_id')
            print(use_id)
            for u_id in use_id:
                use_m = User.objects.filter(id=u_id['user_id']).values('email')
                for u_m in use_m:
                    print(u_m['email'])
                    try:
                        send_mail(
                            subject=subject,
                            message=f'Автор: {instance.to_author}, заголовок: {instance.header_post}, дата выхода: {instance.create_post.strftime("%d %m %Y")}',
                            from_email='katkofff@yandex.ru',
                            recipient_list=[f'{u_m["email"]}', ]
                                    )
                        print(f'send email to {u_m["email"]}')
                    except Exception:
                        print('spam')
    else:
        subject = f'Произошли изменения в статье на которую вы подписаны'
        print('changed')
        print(instance.id)
        cat_id = PostCategory.objects.filter(to_posts_id=instance.id).values('to_categorys_id')
        for c_id in cat_id:
            use_id = CategorySubscribers.objects.filter(category__id=c_id['to_categorys_id']).values('user_id')
            for u_id in use_id:
                use_m = User.objects.filter(id=u_id['user_id']).values('email')
                for u_m in use_m:
                    print(u_m['email'])
                    try:
                        send_mail(
                            subject=subject,
                            message=f'Автор: {instance.to_author}, заголовок: {instance.header_post}, дата изменения: {instance.create_post.strftime("%d %m %Y")}',
                            from_email='katkofff@yandex.ru',
                            recipient_list=[f'{u_m["email"]}', ]
                                    )
                        print(f'send email to {u_m["email"]}')
                    except Exception:
                        print('spam')