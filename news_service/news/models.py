from django.db import models
from django.contrib.auth.models import User

def get_default_author():
    return User.objects.get(username='existing_username')

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def has_comments(self):
        return self.comment_set.exists()
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        app_label = 'news'