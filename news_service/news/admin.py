from django.contrib import admin
from .models import News, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 5


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'pub_date', 'author')
    inlines = [CommentInline]

admin.site.register(News, NewsAdmin)
