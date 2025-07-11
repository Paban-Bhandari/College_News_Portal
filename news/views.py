from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from .models import NewsArticle, Category, UserProfile, Comment

def home(request):
    """Home page view with featured articles"""
    featured_articles = NewsArticle.objects.filter(
        status='published'
    ).order_by('-views', '-published_at')[:6]
    
    categories = Category.objects.all()
    
    context = {
        'featured_articles': featured_articles,
        'categories': categories,
    }
    return render(request, 'home.html', context)

def article_list(request):
    """List all published articles with filtering"""
    articles = NewsArticle.objects.filter(status='published')
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    if category_id:
        articles = articles.filter(category_id=category_id)
    
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(summary__icontains=search_query)
        )
    
    categories = Category.objects.all()
    
    context = {
        'articles': articles,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
    }
    return render(request, 'article_list.html', context)

def article_detail(request, article_id):
    """Display a single article with comments"""
    article = get_object_or_404(NewsArticle, id=article_id, status='published')
    
    # Increment view count
    article.views += 1
    article.save()
    
    # Get approved comments
    comments = article.comments.filter(is_approved=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('comment_content')
        if content:
            Comment.objects.create(
                article=article,
                author=request.user,
                content=content
            )
            messages.success(request, 'Comment submitted successfully!')
            return redirect('article_detail', article_id=article.id)
    
    context = {
        'article': article,
        'comments': comments,
    }
    return render(request, 'article_detail.html', context)

def user_login(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def user_logout(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard(request):
    """User dashboard"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if user_profile.is_editor:
        # Editor dashboard
        user_articles = NewsArticle.objects.filter(author=request.user).order_by('-created_at')
        pending_comments = Comment.objects.filter(is_approved=False).order_by('-created_at')
        
        context = {
            'user_profile': user_profile,
            'user_articles': user_articles,
            'pending_comments': pending_comments,
            'is_editor': True,
        }
    else:
        # Regular user dashboard
        user_articles = NewsArticle.objects.filter(author=request.user).order_by('-created_at')
        user_comments = Comment.objects.filter(author=request.user).order_by('-created_at')
        
        context = {
            'user_profile': user_profile,
            'user_articles': user_articles,
            'user_comments': user_comments,
            'is_editor': False,
        }
    
    return render(request, 'dashboard.html', context)

@login_required
def create_article(request):
    """Create a new article"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        summary = request.POST.get('summary')
        category_id = request.POST.get('category')
        status = request.POST.get('status', 'draft')
        
        if title and content and category_id:
            category = Category.objects.get(id=category_id)
            article = NewsArticle.objects.create(
                title=title,
                content=content,
                summary=summary,
                author=request.user,
                category=category,
                status=status
            )
            messages.success(request, 'Article created successfully!')
            return redirect('article_detail', article_id=article.id)
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'create_article.html', context)

@login_required
def edit_article(request, article_id):
    """Edit an existing article"""
    article = get_object_or_404(NewsArticle, id=article_id, author=request.user)
    
    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.summary = request.POST.get('summary')
        article.category_id = request.POST.get('category')
        article.status = request.POST.get('status', 'draft')
        article.save()
        
        messages.success(request, 'Article updated successfully!')
        return redirect('article_detail', article_id=article.id)
    
    categories = Category.objects.all()
    context = {
        'article': article,
        'categories': categories,
    }
    return render(request, 'edit_article.html', context)

def about(request):
    """About page"""
    return render(request, 'about.html')

def contact(request):
    """Contact page"""
    return render(request, 'contact.html')