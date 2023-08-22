# news/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Comment
from .forms import CommentForm

def news_list(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'news_list': news_list})

def news_detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    comments = Comment.objects.filter(news=news)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news = news
            comment.save()
            return redirect('news_detail', news_id=news_id)

    return render(request, 'news/news_detail.html', {'news': news, 'comments': comments, 'comment_form': comment_form})

def add_news(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        news = News.objects.create(title=title, content=content)
        return redirect('news_detail', news_id=news.id)
    return render(request, 'news/add_news.html')
