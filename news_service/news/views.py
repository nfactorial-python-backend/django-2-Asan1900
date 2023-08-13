from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Comment
from django.shortcuts import render


def news_list(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'news_list': news_list})

def news_detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    comments = Comment.objects.filter(news=news)
    
    if request.method == 'POST':
        content = request.POST['content']
        Comment.objects.create(news=news, content=content)
        return redirect('news_detail', news_id=news_id)
    
    return render(request, 'news/news_detail.html', {'news': news, 'comments': comments})
    
def add_news(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        news = News.objects.create(title=title, content=content)
        return redirect('news_detail', news_id=news.pk)
    
    return render(request, 'news/add_news.html')

def home(request):
    return render(request, 'home.html')