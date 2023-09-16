from django.shortcuts import redirect

def index(request) :
    # 로그인되어 있는 경우, 피드 페이지로 redirect
    if request.user.is_authenticated :
        return redirect('/posts/feeds/')
    # 로그인되어 있지 않은 경우, 로그인 페이지로 redirect
    else :
        return redirect('/users/login/')