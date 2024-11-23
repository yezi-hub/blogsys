from django.contrib.auth import authenticate, login, logout  
from django.contrib.auth.forms import UserCreationForm  
from django.shortcuts import render, redirect,get_object_or_404 
from django.contrib import messages  
from .models import Post  
from .forms import PostForm  
from django.core.paginator import Paginator  
from django.db.models import Q  

from .models import Comment 
from .forms import CommentForm
from django.contrib.auth.decorators import login_required  
from django.contrib.admin.views.decorators import staff_member_required 

from django.http import HttpResponseRedirect 
from django.urls import reverse  

from .utils import truncate_content  # 导入该函数

def post_create(request):  
    # 检查用户是否已登录  
    if not request.user.is_authenticated:  
        return redirect('login')  # 假设'login'是登录 URL 的命名路由  

    if request.method == 'POST':  
        form = PostForm(request.POST)  
        if form.is_valid():  
            post = form.save(commit=False)  #commit=False，先不提交到数据库
            post.author = request.user  #指定一下，博客的作者是当前的当前用户
            post.save()  #把博客的内容再保存到数据库
            return redirect('post_list')  #重定向到博客的列表页面
    else:  #如果是get请求，显示博客的发布页面
        form = PostForm()  
    return render(request, 'blog/post_form.html', {'form': form})  

def post_edit(request, post_id):  
    # 检查用户是否已登录  
    if not request.user.is_authenticated:  
        return redirect('login')  # 假设'login'是登录 URL 的命名路由  

    # 获取要编辑的博客  
    post = get_object_or_404(Post, id=post_id)  

    if request.method == 'POST':  
        form = PostForm(request.POST, instance=post)  # 用实例化表单填充现有博客  
        if form.is_valid():  
            post = form.save(commit=False)  # commit=False，先不提交到数据库  
            post.author = request.user  # 确保作者是当前用户  
            post.is_approved = False  # 标记为未审核通过状态  
            post.save()  # 保存到数据库  
            return redirect('post_list')  # 重定向到博客的列表页面  
    else:  # 如果是GET请求，显示博客的编辑页面  
        form = PostForm(instance=post)  # 填充表单  

    return render(request, 'blog/post_form.html', {'form': form, 'post': post})  

# 博客列表视图  
def post_list(request):  
    query = request.GET.get('q')  
    if query:  
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query),is_approved=True).order_by('-created_at')  
    else:  
        posts = Post.objects.filter(is_approved=True).order_by('-created_at')  

    # 对每个文章内容应用 truncate_content  
    for post in posts:  
        post.truncated_content = truncate_content(post.content)  
        print("&&&&&&&&&&&&&&",post.truncated_content)

    paginator = Paginator(posts, 5)  # 每页显示5条数据  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  
    
    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'query': query})  

#展示博客详情的视图函数
"""
def post_detail(request, post_id):  
    # 从数据库获取正确的博客文章，使用 get_object_or_404  
    post = get_object_or_404(Post, id=post_id)  
    return render(request, 'blog/post_detail.html', {'post': post}) 
"""
def post_detail(request, post_id):  
    post = get_object_or_404(Post, id=post_id)  

    if request.method == 'POST':  
        comment_form = CommentForm(request.POST)  
        if comment_form.is_valid():  
            comment = comment_form.save(commit=False)  
            comment.post = post  
            comment.author = request.user  # 设定评论的作者为当前用户  
            comment.save()  
            messages.success(request, '评论成功！')  
            return redirect('post_detail', post_id=post.id)  
    else:  
        comment_form = CommentForm()  

    # 获取与当前文章关联的所有评论，并进行翻页  
    comments = post.comments.filter(is_approved=True)  
    paginator = Paginator(comments, 5)  # 每页显示5条评论  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'blog/post_detail.html', {  
        'post': post,  
        'comments': page_obj,  # 使用翻页后的评论对象  
        'comment_form': comment_form,  
    })  

# 评论审核视图  
@staff_member_required  
def show_unapproved_comments(request):  
    search_query = request.GET.get('search', '')  
    if search_query:  
        comments = Comment.objects.filter(  
            Q(content__icontains=search_query)  
        ).order_by('-created_at')     
    else:  
        comments = Comment.objects.filter(is_approved=False).order_by('-created_at')  # 默认获取未审核的评论  

    paginator = Paginator(comments, 5)  # 每页显示5条评论  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'blog/comment_review_from_unapproved_comments.html', {'comments': page_obj, 'search_query': search_query})

@staff_member_required  
def show_approved_comments(request):  
    search_query = request.GET.get('search', '')  
    if search_query:  
        comments = Comment.objects.filter(  
            Q(content__icontains=search_query)  
        ).order_by('-created_at')     
    else:  
        comments = Comment.objects.filter(is_approved=True).order_by('-created_at')  # 默认获取未审核的评论  

    paginator = Paginator(comments, 5)  # 每页显示5条评论  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'blog/comment_review_from_approved_comments.html', {'comments': page_obj, 'search_query': search_query})


@staff_member_required  
def show_all_comments(request):  
    search_query = request.GET.get('search', '')  
    if search_query:  
        comments = Comment.objects.filter(  
            Q(content__icontains=search_query)  
        ).order_by('-created_at')    
    else:  
        comments = Comment.objects.all().order_by('-created_at')  # 默认获取未审核的评论  

    paginator = Paginator(comments, 5)  # 每页显示5条评论  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'blog/comment_review_from_all_comments.html', {'comments': page_obj, 'search_query': search_query})



@staff_member_required  
def approve_comment_from_all_comments(request, comment_id):  
    print("------------------------------",comment_id)
    comment = Comment.objects.get(id=comment_id)  
    comment.is_approved = not comment.is_approved  # 切换审核状态  
    comment.save()  
    # Get search parameters  
    search_query = request.GET.get('search', '')  

    # Build redirect URL with the search query  
    return HttpResponseRedirect(f"{reverse('all_comments')}?search={search_query}")    

@staff_member_required  
def approve_comment_from_approved_comments(request, comment_id):  
    comment = Comment.objects.get(id=comment_id)  
    comment.is_approved = not comment.is_approved  # 切换审核状态  
    comment.save()  
    # Get search parameters  
    search_query = request.GET.get('search', '')  

    # Build redirect URL with the search query  
    return HttpResponseRedirect(f"{reverse('approved_comments')}?search={search_query}")    



@staff_member_required  
def approve_comment_from_unapproved_comments(request, comment_id):  
    comment = Comment.objects.get(id=comment_id)  
    comment.is_approved = not comment.is_approved  # 切换审核状态  
    comment.save()  
    # Get search parameters  
    search_query = request.GET.get('search', '')  

    # Build redirect URL with the search query  
    return HttpResponseRedirect(f"{reverse('unapproved_comments')}?search={search_query}")    


# 博客审核视图  
@staff_member_required  
def show_unapproved_posts(request):  
    search_query = request.GET.get('search', '')  
    if search_query:  
        posts = Post.objects.filter(  
            Q(title__icontains=search_query) |   
            Q(content__icontains=search_query)  
        ).order_by('-created_at')   
    else:  
        posts = Post.objects.filter(is_approved=False).order_by('-created_at')   # 默认获取未审核的博客文章  

    paginator = Paginator(posts, 5)  # 每页显示5条文章  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'blog/post_review_from_unapproved_posts.html', {'posts': page_obj, 'search_query': search_query})

@staff_member_required  
def show_all_posts(request):  
    search_query = request.GET.get('search', '')  
    if search_query:  
        posts = Post.objects.filter(  
            Q(title__icontains=search_query) |   
            Q(content__icontains=search_query)  
        ).order_by('-created_at')   
    else:  
        posts = Post.objects.all().order_by('-created_at')   # 默认获取未审核的博客文章  

    paginator = Paginator(posts, 5)  # 每页显示5条文章  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'blog/post_review_from_all_posts.html', {'posts': page_obj, 'search_query': search_query})

@staff_member_required  
def  show_approved_posts(request):  
    search_query = request.GET.get('search', '')  
    if search_query:  
        posts = Post.objects.filter(  
            Q(title__icontains=search_query) |   
            Q(content__icontains=search_query)  
        ) .order_by('-created_at') 
    else:  
        posts = Post.objects.filter(is_approved=True).order_by('-created_at') 
  # 默认获取未审核的博客文章  

    paginator = Paginator(posts, 5)  # 每页显示5条文章  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'blog/post_review_from_approved_posts.html', {'posts': page_obj, 'search_query': search_query})


@staff_member_required  
def approve_post_from_all_posts(request, post_id):  
    post = Post.objects.get(id=post_id)  
    post.is_approved = not post.is_approved  # 切换审核状态  
    post.save()  

    # 获取search参数  
    search_query = request.GET.get('search', '')  

    # Build redirect URL with the search query  
    return HttpResponseRedirect(f"{reverse('all_posts')}?search={search_query}")  

@staff_member_required  
def approve_post_from_approved_posts(request, post_id):  
    post = Post.objects.get(id=post_id)  
    post.is_approved = not post.is_approved  # 切换审核状态  
    post.save()  

    # 获取search参数  
    search_query = request.GET.get('search', '')  

    # Build redirect URL with the search query  
    return HttpResponseRedirect(f"{reverse('approved_posts')}?search={search_query}")  

@staff_member_required  
def approve_post_from_unapproved_posts(request, post_id):  
    post = Post.objects.get(id=post_id)  
    post.is_approved = not post.is_approved  # 切换审核状态  
    post.save()  

    # 获取search参数  
    search_query = request.GET.get('search', '')  

    # Build redirect URL with the search query  
    return HttpResponseRedirect(f"{reverse('unapproved_posts')}?search={search_query}")  


# 用户注册视图  
def register(request):  
    if request.method == 'POST':  
        form = UserCreationForm(request.POST)  
        if form.is_valid():  
            form.save()  
            username = form.cleaned_data.get('username')  
            messages.success(request, f'账号 {username} 注册成功！')  
            return redirect('login')  
    else:  #当请求是get请求的时候触发
        form = UserCreationForm()  
        #使用register.html模板文件，把form类的实例套用在模板文件中，网页中就会出现一个表单
    return render(request, 'blog/register.html', {'form': form})  

# 用户登录视图  
def user_login(request):  
    if request.method == 'POST':  #如果请求是post，就拿到请求中的用户名和密码，进行鉴权
        username = request.POST['username']  
        password = request.POST['password'] 
        # authenticate验证用户名和密码的函数，如果成功返回一个user实例，失败返回None
        user = authenticate(request, username=username, password=password)  
        if user is not None:  #返回的不是None，说明登录成功
            login(request, user)  #使用user的实例，进行登录，获取一个成功的user登录状态
            print("登录成功")
            return redirect('post_list')  #重定向到首页 
        else: 
            print("登录失败！")
            return render(request, 'blog/login.html',{"message":"登录失败，用户名或者密码错误！"})
    else:
        return render(request, 'blog/login.html')  #如果失败了，就返回到登录页面

def home(request):
    return render(request, 'blog/home.html') 

@login_required 
def show_my_blogs(request):
    query = request.GET.get('q')  
    if query: 
        # 确保用户已登录  
        if request.user.is_authenticated:   
            posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query),author=request.user).order_by('-created_at')
        else:
            posts = []   
    else:  
        # 确保用户已登录  
        if request.user.is_authenticated:   
            posts = Post.objects.filter(author=request.user).order_by('-created_at')
        else:
            posts = [] 

    # 对每个文章内容应用 truncate_content  
    for post in posts:  
        post.truncated_content = truncate_content(post.content)  
        print("&&&&&&&&&&&&&&",post.truncated_content)    

    paginator = Paginator(posts, 5)  # 每页显示5条数据  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  
    
    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'query': query})    

# 用户退出视图  
def user_logout(request):  
    logout(request)  
    return redirect('login')  #访问到登录页面