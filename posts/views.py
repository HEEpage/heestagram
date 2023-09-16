from django.shortcuts import render, redirect

def feeds(request) :
    # 로그인한 사용자가 아닐 경우 (AnonymousUser인 경우)
    if not request.user.is_authenticated :
        # /users/login/으로 이동
        return redirect('/users/login/')

    return render(request, 'posts/feeds.html')
