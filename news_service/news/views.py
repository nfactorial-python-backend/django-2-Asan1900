# news/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Comment
from .forms import CommentForm, NewsForm
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy


class NewsUpdateView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news:news_detail')


def news_list(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            return redirect('news:news_detail', news_id=news.id)
    else:
        form = NewsForm()
    
    context = {'form': form}
    return render(request, 'news/news_list.html', context)

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
            return redirect('news:news_detail', news_id=news_id)

    return render(request, 'news/news_detail.html', {'news': news, 'comments': comments, 'comment_form': comment_form})
def add_news(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        news = News.objects.create(title=title, content=content)
        return redirect('news:news_detail', news_id=news.id) 
    return render(request, 'news/add_news.html')
