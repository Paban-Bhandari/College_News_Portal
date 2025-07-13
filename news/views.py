from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .forms import CustomUserCreationForm
from .models import NewsArticle, Category, UserProfile, Like, Comment

def get_client_ip(request):
    """Get the client's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
    # Try to get the article
    try:
        article = NewsArticle.objects.get(id=article_id)
        
        # Check if user can view this article
        can_view = False
        
        # Published articles can be viewed by anyone
        if article.status == 'published':
            can_view = True
        # Draft/archived articles can only be viewed by the author
        elif request.user.is_authenticated and article.author == request.user:
            can_view = True
        
        if not can_view:
            raise NewsArticle.DoesNotExist()
            
    except NewsArticle.DoesNotExist:
        return get_object_or_404(NewsArticle, id=article_id, status='published')
    
    # Increment view count only for published articles
    if article.status == 'published':
        article.views += 1
        article.save()
    
    # Get approved comments
    comments = article.comments.filter(is_approved=True)
    
    # Check if user has liked the article
    user_liked = False
    if request.user.is_authenticated:
        user_liked = article.likes.filter(user=request.user).exists()
    else:
        # Check for anonymous like by IP
        client_ip = get_client_ip(request)
        user_liked = article.likes.filter(ip_address=client_ip, user__isnull=True).exists()
    
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('comment_content')
        
        if content:
            Comment.objects.create(
                article=article,
                author=request.user,
                content=content,
                is_approved=True  # Auto-approve comments
            )
            messages.success(request, 'Comment submitted successfully!')
            return redirect('article_detail', article_id=article.id)
    
    context = {
        'article': article,
        'comments': comments,
        'user_liked': user_liked,
    }
    return render(request, 'article_detail.html', context)

@require_POST
def toggle_like(request, article_id):
    """Toggle like/unlike for an article"""
    article = get_object_or_404(NewsArticle, id=article_id)
    
    if request.user.is_authenticated:
        # Logged in user
        like, created = Like.objects.get_or_create(
            article=article,
            user=request.user,
            defaults={'user': request.user}
        )
        
        if not created:
            # Unlike
            like.delete()
            liked = False
        else:
            # Like
            liked = True
    else:
        # Anonymous user - just use IP address
        client_ip = get_client_ip(request)
        
        # Check if anonymous user already liked this article
        existing_like = Like.objects.filter(
            article=article,
            ip_address=client_ip,
            user__isnull=True
        ).first()
        
        if existing_like:
            # Unlike
            existing_like.delete()
            liked = False
        else:
            # Like
            Like.objects.create(
                article=article,
                ip_address=client_ip
            )
            liked = True
    
    return JsonResponse({
        'liked': liked,
        'like_count': article.like_count
    })

@login_required
@require_POST
def add_comment(request, article_id):
    """Add a comment to an article - login required"""
    article = get_object_or_404(NewsArticle, id=article_id)
    content = request.POST.get('content')
    
    if content:
        comment = Comment.objects.create(
            article=article,
            author=request.user,
            content=content,
            is_approved=True  # Auto-approve comments
        )
        
        # Format timestamp to match the template format with timezone
        formatted_time = timezone.localtime(comment.created_at).strftime('%b %d, %Y %H:%M')
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'author': comment.author.username,
                'content': comment.content,
                'created_at': formatted_time,
                'is_approved': comment.is_approved
            }
        })
    
    return JsonResponse({'success': False, 'error': 'Comment content is required'})

@login_required
@require_POST
def edit_comment(request, comment_id):
    """Edit a comment - only comment author can edit"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user is the comment author
    if comment.author != request.user:
        return JsonResponse({'success': False, 'error': 'You can only edit your own comments.'})
    
    content = request.POST.get('content')
    if content:
        comment.content = content
        comment.save()
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'updated_at': comment.created_at.strftime('%B %d, %Y %H:%M')
            }
        })
    
    return JsonResponse({'success': False, 'error': 'Comment content is required'})

@login_required
@require_POST
def delete_comment(request, comment_id):
    """Delete a comment - only comment author can delete"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user is the comment author
    if comment.author != request.user:
        return JsonResponse({'success': False, 'error': 'You can only delete your own comments.'})
    
    comment.delete()
    return JsonResponse({'success': True})

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

def user_register(request):
    """Handle user registration for commenting"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a user profile for the new user
            UserProfile.objects.create(
                user=user,
                is_editor=False,  # Normal users are not editors by default
                bio=''
            )
            # Log the user in after registration
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.first_name}! You can now comment on articles.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def logout_confirm(request):
    """Show logout confirmation page"""
    if not request.user.is_authenticated:
        return redirect('home')
    return render(request, 'logout_confirm.html')

def forgot_password(request):
    """Handle forgot password - reset to Default123"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(username=username, email=email)
            # Reset password to Default123
            user.password = make_password('Default123')
            user.save()
            messages.success(request, f'Password reset successfully! Your new password is: Default123')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No user found with the provided username and email combination.')
        except Exception as e:
            messages.error(request, 'An error occurred while resetting your password. Please try again.')
    
    return render(request, 'forgot_password.html')

def user_logout(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard(request):
    """User dashboard"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get user articles and comments for both editors and regular users
    user_articles = NewsArticle.objects.filter(author=request.user).order_by('-created_at')
    user_comments = Comment.objects.filter(author=request.user).order_by('-created_at')
    
    if user_profile.is_editor:
        # Editor dashboard
        context = {
            'user_profile': user_profile,
            'user_articles': user_articles,
            'user_comments': user_comments,
            'is_editor': True,
        }
    else:
        # Regular user dashboard
        context = {
            'user_profile': user_profile,
            'user_articles': user_articles,
            'user_comments': user_comments,
            'is_editor': False,
        }
    
    return render(request, 'dashboard.html', context)

@login_required
def create_article(request):
    """Create a new article - only for approved editors"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if not user_profile.is_editor:
        messages.error(request, 'You need admin approval to create articles. Please contact the administrator.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        summary = request.POST.get('summary')
        category_id = request.POST.get('category')
        status = request.POST.get('status', 'draft')
        featured_image = request.FILES.get('featured_image')
        
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
            
            # Handle featured image upload
            if featured_image:
                # Validate file type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
                if featured_image.content_type in allowed_types:
                    article.featured_image = featured_image
                    article.save()
                else:
                    messages.error(request, 'Please upload a valid image file (JPG, PNG, or GIF).')
                    return redirect('create_article')
            
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
        
        # Handle featured image upload
        featured_image = request.FILES.get('featured_image')
        if featured_image:
            # Validate file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if featured_image.content_type in allowed_types:
                article.featured_image = featured_image
            else:
                messages.error(request, 'Please upload a valid image file (JPG, PNG, or GIF).')
                return redirect('edit_article', article_id=article.id)
        
        article.save()
        
        messages.success(request, 'Article updated successfully!')
        return redirect('article_detail', article_id=article.id)
    
    categories = Category.objects.all()
    context = {
        'article': article,
        'categories': categories,
    }
    return render(request, 'edit_article.html', context)

@login_required
def delete_article(request, article_id):
    """Delete an article - only the author can delete"""
    article = get_object_or_404(NewsArticle, id=article_id, author=request.user)
    
    if request.method == 'POST':
        article_title = article.title
        article.delete()
        messages.success(request, f'Article "{article_title}" has been deleted successfully!')
        return redirect('dashboard')
    
    # If it's a GET request, show confirmation page
    return render(request, 'delete_article_confirm.html', {'article': article})

def about(request):
    """About page"""
    return render(request, 'about.html')

@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})

def contact(request):
    """Contact page"""
    return render(request, 'contact.html')