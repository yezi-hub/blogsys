
from django import forms  
from .models import Post  
from .models import Comment  
from django.conf import settings
from urllib.parse import urljoin



class PostForm(forms.ModelForm):  
    class Meta:  
        model = Post  
        fields = ['title', 'content','video_url']
        labels = {  
            'title': '标题',  
            'content': '正文',  
            'video_url':"网络视频 url 地址"
        }  

    def clean_video_url(self):  
        if self.cleaned_data.get('video_url', '') is not None:
            video_url = self.cleaned_data.get('video_url', '').strip() 
        else:
            video_url =""
        
        # 如果视频URL为空，允许为空  
        if not video_url:  
            return video_url  
        
        # 检查是否是完整的URL  
        if not video_url.startswith(('http://', 'https://')):  
            try:  
                # 尝试使用站点的基础URL补全相对路径  
                # 方法1：使用 settings 中的站点URL  
                if hasattr(settings, 'SITE_URL'):  
                    video_url = urljoin(settings.SITE_URL, video_url)  
                
                # 方法2：如果没有设置 SITE_URL，可以使用静态文件URL  
                elif hasattr(settings, 'STATIC_URL'):  
                    video_url = urljoin(settings.STATIC_URL, video_url)  
                
            except Exception as e:  
                # 如果URL处理失败，抛出验证错误  
                raise forms.ValidationError(f"无效的视频URL: {str(e)}")  
        
        # 额外的URL有效性检查  
        if not video_url.startswith(('http://', 'https://')):  
            raise forms.ValidationError("请提供一个有效的完整URL地址")  
        
        return video_url  

class CommentForm(forms.ModelForm):  
    class Meta:  
        model = Comment  
        fields = ['content']  
