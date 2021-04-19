from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from news.models import Post, PostCategory, Category, CategorySubscribers
from django.contrib.auth.models import User


def posts_senders():
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
                msg.send()
                print('Рассылка успешна отправлена')
