from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone

from .models import Category, Article
from .views import HomePageView, ArticleList, ArticleCategoryList, ArticleDetail


class UrlsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category='Тестова категорія',
            slug='test-category'
        )
        self.article = Article.objects.create(
            title='Тестова стаття',
            slug='test-article',
            category=self.category,
            pub_date=timezone.now(),
            main_page=True
        )

    def test_home_url_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, HomePageView)

    def test_articles_list_url_status_code(self):
        url = reverse('articles-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_articles_list_url_resolves(self):
        view = resolve('/articles/')
        self.assertEqual(view.func.view_class, ArticleList)

    def test_category_list_url_status_code(self):
        url = reverse('articles-category-list', args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_list_url_resolves(self):
        view = resolve(f'/articles/category/{self.category.slug}')
        self.assertEqual(view.func.view_class, ArticleCategoryList)

    def test_article_detail_url_status_code(self):
        url = self.article.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_article_detail_url_resolves(self):
        url = self.article.get_absolute_url()
        view = resolve(url)
        self.assertEqual(view.func.view_class, ArticleDetail)