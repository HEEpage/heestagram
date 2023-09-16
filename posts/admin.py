from django.contrib import admin
import admin_thumbnails

from posts.models import Post, PostImage, Comment


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


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin) :
    list_display = ['id', 'post', 'photo',]


@admin.register(Comment)
class CommentImageAdmin(admin.ModelAdmin) :
    list_display = ['id', 'post', 'content',]