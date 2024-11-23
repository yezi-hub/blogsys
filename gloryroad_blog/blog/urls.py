from django.urls import path  
from .views import register,user_login,home,user_logout
from .views import post_create,post_list,post_detail
from .views import approve_comment_from_all_comments,approve_comment_from_approved_comments,approve_comment_from_unapproved_comments
from .views import show_my_blogs,post_edit

from .views import show_all_posts
from .views import show_unapproved_posts
from .views import show_approved_posts

from .views import approve_post_from_all_posts
from .views import approve_post_from_approved_posts
from .views import approve_post_from_unapproved_posts


from .views import show_all_comments,show_unapproved_comments,show_approved_comments

urlpatterns = [  
    path('register/', register, name='register'),  
    path('login/', user_login, name='login'),  
    path('logout/', user_logout, name='logout'),  
    path('home/', home, name='home'),  
    path('posts/new/', post_create, name='post_create'), 
    path('post/edit/<int:post_id>/', post_edit,name="post_edit"),
    path('posts/list/', post_list, name='post_list'), 
    path('posts/<int:post_id>/', post_detail, name='post_detail'),  # 详情页面路由
    path('posts/myblogs/', show_my_blogs, name='my_blogs'),  # 详情页面路由   

    path('comments/all_comments/', show_all_comments, name='all_comments'),  
    path('comments/unapproved_comments/', show_unapproved_comments, name='unapproved_comments'),  
    path('comments/approved_comments/', show_approved_comments, name='approved_comments'),  

    path('comments/approve_comment_from_all_comments/<int:comment_id>/', approve_comment_from_all_comments, name='approve_comment_from_all_comments'),  
    path('comments/approve_comment_from_approved_comments/<int:comment_id>/', approve_comment_from_approved_comments, name='approve_comment_from_approved_comments'), 
    path('comments/approve_comment_from_unapproved_comments/<int:comment_id>/', approve_comment_from_unapproved_comments, name='approve_comment_from_unapproved_comments'), 


    path('posts/all_posts/', show_all_posts, name='all_posts'), 
    path('posts/unapproved_posts/', show_unapproved_posts,name='unapproved_posts'), 
    path('posts/approved_posts/', show_approved_posts, name='approved_posts'), 

    path('posts/approve_post_from_all_posts/<int:post_id>/', approve_post_from_all_posts, name='approve_post_from_all_posts'),  
    path('posts/approve_post_from_approved_posts/<int:post_id>/', approve_post_from_approved_posts, name='approve_post_from_approved_posts'), 
    path('posts/approve_post_from_unapproved_posts/<int:post_id>/', approve_post_from_unapproved_posts, name='approve_post_from_unapproved_posts'), 
]


