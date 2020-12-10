from django.contrib import admin
from .models import Author, Category, Article, Comment, NestedComment, Image


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['author', 'slug', 'date_created']
    list_filter = ['date_created']
    list_editable = ['slug']
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('comment',)}


class NestedCommentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('comment',)}


admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(NestedComment, NestedCommentAdmin)
admin.site.register(Image)
