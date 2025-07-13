from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, NewsArticle, UserProfile, Like, Comment
from django.utils import timezone


class NewsModelsTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
        self.article = NewsArticle.objects.create(
            title='Test Article',
            content='Test article content',
            summary='Test summary',
            author=self.user,
            category=self.category,
            status='published',
            published_at=timezone.now()
        )

    def test_category_str(self):
        """Test Category string representation"""
        self.assertEqual(str(self.category), 'Test Category')

    def test_article_str(self):
        """Test NewsArticle string representation"""
        self.assertEqual(str(self.article), 'Test Article')

    def test_article_like_count(self):
        """Test article like count property"""
        self.assertEqual(self.article.like_count, 0)
        
        # Add a like
        Like.objects.create(article=self.article, user=self.user)
        self.assertEqual(self.article.like_count, 1)

    def test_article_comment_count(self):
        """Test article comment count property"""
        self.assertEqual(self.article.comment_count, 0)
        
        # Add an approved comment
        Comment.objects.create(
            article=self.article,
            author=self.user,
            content='Test comment',
            is_approved=True
        )
        self.assertEqual(self.article.comment_count, 1)

    def test_user_profile_creation(self):
        """Test UserProfile is created automatically for new users"""
        new_user = User.objects.create_user(
            username='newuser',
            password='pass123'
        )
        profile = UserProfile.objects.get(user=new_user)
        self.assertIsNotNone(profile)
        self.assertFalse(profile.is_editor)


class NewsViewsTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
        self.article = NewsArticle.objects.create(
            title='Test Article',
            content='Test article content',
            summary='Test summary',
            author=self.user,
            category=self.category,
            status='published',
            published_at=timezone.now()
        )

    def test_home_page(self):
        """Test home page loads correctly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')

    def test_article_list_page(self):
        """Test article list page loads correctly"""
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')

    def test_article_detail_page(self):
        """Test article detail page loads correctly"""
        response = self.client.get(reverse('article_detail', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')

    def test_login_page(self):
        """Test login page loads correctly"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        """Test register page loads correctly"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_with_login(self):
        """Test dashboard loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
