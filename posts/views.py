from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden

from posts.models import Post, Comment
from posts.forms import CommentForm

def feeds(request) :
    # 로그인한 사용자가 아닐 경우 (AnonymousUser인 경우)
    if not request.user.is_authenticated :
        # /users/login/으로 이동
        return redirect('/users/login/')
    
    # 모든 글 목록을 템플릿으로 전달
    posts = Post.objects.all()
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
        return HttpResponseRedirect(f'/posts/feeds/#post-{comment.post.id}')


@require_POST
def comment_delete(request, comment_id) :
    comment = Comment.objects.get(id=comment_id)

    if comment.user == request.user :
        comment.delete()
        return HttpResponseRedirect(f'/posts/feeds/#post-{comment.post.id}')
    else :
        return HttpResponseForbidden('이 댓글을 삭제할 권한이 없습니다.')