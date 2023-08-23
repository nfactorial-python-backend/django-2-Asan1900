# news/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import News, Comment

class NewsViewsTestCase(TestCase):
    def setUp(self):
        self.news = News.objects.create(title='Test News', content='Test content')
        self.comment = Comment.objects.create(news=self.news, content='Test comment')

    def test_news_list_view(self):
        response = self.client.get(reverse('news:new_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['new_list'],
            [str(self.news)],
            transform=str
        )

    def test_news_detail_view(self):
        response = self.client.get(reverse('news:news_detail', args=(self.news.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['news'], self.news)

    def test_news_detail_view_with_comments(self):
        response = self.client.get(reverse('news:news_detail', args=(self.news.id,)))
        self.assertContains(response, 'Test comment')

    def test_news_detail_view_without_comments(self):
        self.comment.delete()
        response = self.client.get(reverse('news:news_detail', args=(self.news.id,)))
        self.assertNotContains(response, 'Test comment')
