from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

from posts.models import Post, Comment, PostImage, HashTag
from posts.forms import CommentForm, PostForm

def feeds(request) :
    # 로그인한 사용자가 아닐 경우 (AnonymousUser인 경우)
    if not request.user.is_authenticated :
        # /users/login/으로 이동
        return redirect('users:login')
    
    # 모든 글 목록을 템플릿으로 전달
    posts = Post.objects.all().order_by('-created')
    comment_form = CommentForm()

    context = {
        'posts' : posts,
        'comment_form' : comment_form,
    }

    return render(request, 'posts/feeds.html', context)


# 댓글 작성을 처리할 View. POST 요청만 허용한다.
@require_POST
def comment_add(request) :
    # request.POST로 전달된 데이터를 사용해 CommentForm 인스턴스를 생성
    form = CommentForm(data=request.POST)

    if form.is_valid() :
        # commit=False 옵션으로 메모리상에 Comment 객체 생성
        comment = form.save(commit=False)
        # Comment 생성에 필요한 사용자 정보를 request에서 가져와 할당
        comment.user = request.user
        # DB에 Comment 객체 저장
        comment.save()

        # 생성 완료 후 피드 페이지로 이동
        # redirect() 함수가 아닌 HttpResponseRedirect는 URL pattern name을 사용할 수 없다.
        # 이 경우, reverse() 함수로 URL을 만든 후, 뒤에 추가로 붙일 주소를 직접 입력해야 한다.
        url = reverse('posts:feeds') + f'#post-{comment.post.id}'
        return HttpResponseRedirect(url)


@require_POST
def comment_delete(request, comment_id) :
    comment = Comment.objects.get(id=comment_id)

    if comment.user == request.user :
        comment.delete()
        url = reverse('posts:feeds') + f'#post-{comment.post.id}'
        return HttpResponseRedirect(url)
    else :
        return HttpResponseForbidden('이 댓글을 삭제할 권한이 없습니다.')


def post_add(request) :
    if request.method == 'POST' :
        # request.POST로 온 데이터('content')는 PostForm으로 처리
        form = PostForm(request.POST)

        if form.is_valid() :
            # Post의 'user' 값은 request에서 가져와 할당한다.
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # Post를 생성한 후, 
            # request.FILES.getlist('images')로 전송된 이미지들을 순회하며
            # PostImage 객체를 생성한다.
            for image_file in request.FILES.getlist('images') :
                # request.FILES 또는 request.FILES.getlist()로 가져온 파일은
                # Model의 ImageField 부분에 곧바로 할당한다.
                PostImage.objects.create(
                    post = post,
                    photo = image_file,
                )
            
            # 'tags'에 전달된 문자열을 분리해 HashTag 생성
            tag_string = request.POST.get('tags')
            if tag_string :
                tag_names = [ tag_name.strip() for tag_name in tag_string.split(',') ]
                for tag_name in tag_names :
                    tag, _ = HashTag.objects.get_or_create(name=tag_name)
                    # get_or_create로 생성하거나 가져온 HashTag 객체를 Post의 tags에 추가한다.
                    post.tags.add(tag)
            
            # 모든 PostImage와 Post 생성이 완료되면
            # 피드 페이지로 이동하여 생성된 Post의 위치로 이동하도록 한다.
            url = reverse('posts:feeds') + f'#post-{post.id}'
            return HttpResponseRedirect(url)
    
    # GET 요청일 때는 빈 form을 보여주도록 한다.
    else :
        form = PostForm()
    
    context = {
        'form' : form,
    }
    return render(request, 'posts/post_add.html', context)


def tags(request, tag_name) :
    try :
        tag = HashTag.objects.get(name=tag_name)
    except HashTag.DoesNotExist :
        # tag_name에 해당하는 HashTag를 찾지 못한 경우, 빈 QuerySet을 돌려준다.
        posts = Post.objects.none()
    else :
        # tags(ManyToMany 필드)에 찾은 HashTag 객체가 있는 Post들을 필터
        posts = Post.objects.filter(tags=tag)

    # context로 Template에 필터링된 Post QuerySet을 넘겨주며
    # 어떤 tag_name으로 검색했는지도 넘겨준다.
    context = {
        'tag_name' : tag_name,
        'posts' : posts,
    }
    return render(request, 'posts/tags.html', context)