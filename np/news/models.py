from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    to_user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating_author=models.IntegerField(default = 0)    
    def update_rating(self):
        self.rating_author=0
        self.save()
        posts = Post.objects.filter(to_author__to_user__id=self.id)
        value_post = sum([p['rating_post']*3 for p in posts.values()])
        comment_own = sum([c['comment_rating'] for c in Comment.objects.filter(comment_to_user__id=self.id).values()])
        comment_other = sum([c['comment_rating'] for c in Comment.objects.filter(comment_to_post__in = posts).values()]) 
        self.rating_author=value_post+comment_own+comment_other
        self.save()
    def __str__(self):
        return self.to_user.username
        
class Category(models.Model):
    name=models.CharField(max_length = 255,unique=True)

class Post(models.Model):
    article='AR'
    news='NE'
    CATEGORYS=[(article,'статья'),
               (news,'новость')]
    to_author=models.ForeignKey(Author, on_delete = models.CASCADE)
    category_post = models.CharField(max_length = 2, 
                                     choices = CATEGORYS, 
                                     default = article)
    create_post=models.DateTimeField(auto_now_add = True)
    to_category=models.ManyToManyField(Category, through = 'PostCategory')
    header_post=models.CharField(max_length = 255)
    content_post=models.TextField()
    rating_post=models.IntegerField(default = 0)
    
    def like(self,value):
        self.rating_post+=value
        self.save()
    def dislike(self,value):
        self.rating_post-=value
        self.save()
    def preview(self):
        if len(self.content_post)>124:
            prev=self.content_post[0:124]+'...'
        else:
            prev=self.content_post+'...'
        return prev
        
class PostCategory(models.Model):
    to_post=models.ForeignKey(Post, on_delete = models.CASCADE)
    to_category=models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    comment_to_post=models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_to_user=models.ForeignKey(User, on_delete = models.CASCADE)
    comment_text=models.TextField()
    comment_time=models.DateTimeField(auto_now_add = True)
    comment_rating=models.IntegerField(default = 0)
    
    def like(self,value):
        self.comment_rating+=value
        self.save()
    def dislike(self,value):
        self.comment_rating-=value
        self.save()
 