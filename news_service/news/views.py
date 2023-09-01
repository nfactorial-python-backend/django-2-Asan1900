# news/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Comment
from .forms import CommentForm, NewsForm
from django.views.generic.edit import UpdateView, CreateView 
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView

def home_page(request):
    return render(request, 'news/home.html')

class SignUpView(CreateView):  
    template_name = 'registration/sign_up.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('news:news_list')

    def form_valid(self, form):
        user = form.save()
        if self.request.POST.get('is_moderator'):
            user.groups.add(Group.objects.get(name='moderators'))
        else:
            user.groups.add(Group.objects.get(name='default'))
        login(self.request, user)
        return super().form_valid(form)
    
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class NewsUpdateView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news:news_detail')

@login_required
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

@login_required
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

@permission_required('news.add_news')
def add_news(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        news = News.objects.create(title=title, content=content)
        return redirect('news:news_detail', news_id=news.id) 
    return render(request, 'news/add_news.html')

@permission_required('news.delete_news')
def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if news.author == request.user or request.user.groups.filter(name='moderators').exists():
        news.delete()
        return redirect('news:news_list')
    else:
        return('You don not have access for that')

@permission_required('news.delete_comment')
def delete_comment(request, news_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user or request.user.groups.filter(name='moderators').exists():
        comment.delete()
        return redirect('news:news_detail', news_id=news_id)
    else:
        return('You don not have access for that')

@permission_required('news.change_news')
def edit_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news:news_detail', news_id=news_id)
    else:
        form = NewsForm(instance=news)
    
    return render(request, 'news/edit_news.html', {'form': form, 'news': news})

@permission_required('news.add_comment')
def add_comment(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news = news
            comment.author = request.user  # Assign the current user as the author
            comment.save()
            return redirect('news:news_detail', news_id=news_id)
    else:
        comment_form = CommentForm()

    return render(request, 'news/add_comment.html', {'news': news, 'comment_form': comment_form})
