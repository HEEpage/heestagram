from django.shortcuts import render, redirect

from posts.models import Post

def feeds(request) :
    # 로그인한 사용자가 아닐 경우 (AnonymousUser인 경우)
    if not request.user.is_authenticated :
        # /users/login/으로 이동
        return redirect('/users/login/')
    
    # 모든 글 목록을 템플릿으로 전달
    posts = Post.objects.all()
    context = {
        'posts' : posts,
    }

    return render(request, 'posts/feeds.html', context)
