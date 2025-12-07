from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone

from .views import HomePageView, ArticleList, ArticleCategoryList, ArticleDetail
from .models import Category, Article


class HomeTests(TestCase):

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, HomePageView)


class ArticlesUrlsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # створюємо тестові дані один раз для всіх тестів цього класу
        cls.category = Category.objects.create(
            category='News',
            slug='news',
        )
        cls.article = Article.objects.create(
            title='Test article',
            description='Some test body',
            pub_date=timezone.now(),
            slug='test-article',
            main_page=True,
            category=cls.category,
        )

    def test_articles_list_status_code(self):
        """Список усіх публікацій /articles"""
        url = reverse('articles-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_articles_list_resolves_view(self):
        view = resolve('/articles')
        self.assertEqual(view.func.view_class, ArticleList)

    def test_category_view_status_code(self):
        url = reverse('articles-category-list', args=(self.category.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_url_resolves_view(self):
        path = f'/articles/category/{self.category.slug}'
        view = resolve(path)
        self.assertEqual(view.func.view_class, ArticleCategoryList)

    def test_article_detail_status_code(self):
        url = self.article.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_article_detail_url_resolves_view(self):
        path = self.article.get_absolute_url()
        view = resolve(path)
        self.assertEqual(view.func.view_class, ArticleDetail)
