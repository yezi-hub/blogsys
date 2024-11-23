
from django.db import models  
from django.contrib.auth.models import User  
from ckeditor.fields import RichTextField 

class Post(models.Model):  
    title = models.CharField(max_length=200)  
    content = RichTextField() 
    video_url = models.CharField(max_length=500, blank=True, null=True)  
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True) 
    is_approved = models.BooleanField(default=False)  # 新增字段  

 

class Comment(models.Model):  
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    is_approved = models.BooleanField(default=False)  # 新增字段  

    def __str__(self):  
        return f'{self.author.username} - {self.created_at}'  