from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from users.forms import LoginForm, SignupForm
from users.models import User

def login_view(request) :
    # 이미 로그인되어 있다면
    if request.user.is_authenticated :
        return redirect('posts:feeds')
    
    if request.method == 'POST' :
        # LoginForm 인스턴스를 만들며, 입력 데이터는 request.POST를 사용
        form = LoginForm(data=request.POST)

        # LoginForm에 전달된 데이터가 유효하다면
        if form.is_valid() :
            # username과 password 값을 가져와서 변수에 할당
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # username, password에 해당하는 사용자가 있는지 검사
            user = authenticate(username=username, password=password)

            # 해당 사용자가 존재하면
            if user :
                # 로그인 처리 후, 피드 페이지로 redirect
                login(request, user)
                return redirect('posts:feeds')
            # 해당 사용자가 없다면 form에 에러 추가
            else :
                form.add_error(None, '입력한 자격증명에 해당하는 사용자가 없습니다.')

        # 어떤 경우든 실패한 경우(데이터 검증, 사용자 검사) 다시 LoginForm을 사용한 로그인 페이지 렌더링
        context = {
            'form' : form,
        }
        return render(request, 'users/login.html', context)
        
    else :
        form = LoginForm()
        context = {
            'form' : form,
        }
        return render(request, 'users/login.html', context)


def logout_view(request) :
    # logout 함수 호출에 request를 전달한다
    logout(request)
    # logout 처리 후, 로그인 페이지로 이동한다
    return redirect('users:login')


def signup(request) :
    # POST 요청 시, form이 유효하다면 최종적으로 redirect 처리된다.
    if request.method == 'POST' :
        form = SignupForm(data=request.POST, files=request.FILES)
        
        # Form에 에러가 없다면 User를 생성하고 로그인 페이지로 이동한다.
        if form.is_valid() :
            form.save()
            return redirect('users:login')

        # POST 요청에서 Form이 유효하지 않다면, 아래의 context = ... 부분으로 이동한다.

    # GET 요청 시, 빈 Form을 생성한다.
    else :
        form = SignupForm()
    
    # context로 전달되는 form은 두 가지 경우가 존재한다.
    # 1. POST 요청에서 생성된 form이 유효하지 않은 경우 -> 에러를 포함한 form이 사용자에게 보여진다.
    # 2. GET 요청으로 빈 form이 생성된 경우 -> 빈 form이 사용자에게 보여진다.
    context = {
        'form' : form,
    }
    return render(request, 'users/signup.html', context)


def profile(request, user_id) :
    user = get_object_or_404(User, id=user_id)
    context = {
        'user' : user,
    }
    return render(request, 'users/profile.html', context)


def followers(request, user_id) :
    user = get_object_or_404(User, id=user_id)
    relationships = user.follower_relationships.all()

    context = {
        'user' : user,
        'relationships' : relationships,
    }
    return render(request, 'users/followers.html', context)


def following(request, user_id) :
    user = get_object_or_404(User, id=user_id)
    relationships = user.following_relationships.all()

    context = {
        'user' : user,
        'relationships' : relationships,
    }
    return render(request, 'users/following.html', context)