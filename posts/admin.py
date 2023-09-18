from django.contrib import admin
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple
import admin_thumbnails

from posts.models import Post, PostImage, Comment, HashTag


class CommentInline(admin.TabularInline) :
    model = Comment
    extra = 1

@admin_thumbnails.thumbnail('photo')
class PostImageInline(admin.TabularInline) :
    model = PostImage
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin) :
    list_display = ['id', 'content',]
    # ForeignKey로 연결된 Comment 객체 확인하기 위해 admin의 Inline 기능 사용
    inlines = [CommentInline, PostImageInline,] 

    # Post 변경 화면에서 ManyToMayField를 Checkbox로 출력
    formfield_overrides = {
        ManyToManyField : {'widget' : CheckboxSelectMultiple},
    }


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin) :
    list_display = ['id', 'post', 'photo',]


@admin.register(Comment)
class CommentImageAdmin(admin.ModelAdmin) :
    list_display = ['id', 'post', 'content',]


@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin) :
    pass