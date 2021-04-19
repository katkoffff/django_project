from celery import shared_task
from django.core.mail import send_mail
from .models import Post, User, CategorySubscribers, Category, PostCategory
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.utils.timezone import localtime

@shared_task
def send_weekly_news():
    print('Start')
    if datetime.isoweekday(datetime.now()) == 1:
        week = localtime() - timedelta(days=7)
        categories = Category.objects.all()
        for category in categories:
            subscribers = User.objects.filter(categorysubscribers__category=category)
            subscribers_emails = []
            for user in subscribers:
                subscribers_emails.append(user.email)
                post_list = Post.objects.filter(postcategory__to_categorys=category, create_post__gt=week)
                html_content = render_to_string('news_app/weekly_newsletter.html',
                                                {'posts': post_list, 'category': category, })
                msg = EmailMultiAlternatives(
                    subject=f'Все новости за прошедшую неделю',
                    from_email='katkofff@yandex.ru',
                    to=subscribers_emails,
                )
                msg.attach_alternative(html_content, "text/html")
                try:
                    msg.send()
                    print('Рассылка успешна отправлена')
                except Exception:
                    print('spam')

@shared_task
def send_created_category(oid):
    post = Post.objects.get(pk=oid)
    category = Category.objects.get(name=post.name_category())
    subscribers = User.objects.filter(categorysubscribers__category=category)
    subscribers_emails = []
    for user in subscribers:
        subscribers_emails.append(user.email)
        post_list = [post]  #Post.objects.filter(postcategory__to_categorys=category, pk=oid)
        html_content = render_to_string('news_app/callback_newsletter.html',
                                        {'posts': post_list, 'category': category, })
        msg = EmailMultiAlternatives(
            subject=f'В вашей любимой категории новая статья',
            from_email='katkofff@yandex.ru',
            to=subscribers_emails,
        )
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
            print('Рассылка успешна отправлена')
        except Exception:
            print('spam')
