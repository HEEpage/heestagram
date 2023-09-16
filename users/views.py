from django.shortcuts import render, redirect

def login_view(request) :
    # 이미 로그인되어 있다면
    if request.user.is_authenticated :
        return redirect('/posts/feeds/')
    
    return render(request, 'users/login.html')
