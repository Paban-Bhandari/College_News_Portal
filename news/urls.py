from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('article/<int:article_id>/like/', views.toggle_like, name='toggle_like'),
    path('article/<int:article_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('login/', views.user_login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('logout-confirm/', views.logout_confirm, name='logout_confirm'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-article/', views.create_article, name='create_article'),
    path('edit-article/<int:article_id>/', views.edit_article, name='edit_article'),
    path('delete-article/<int:article_id>/', views.delete_article, name='delete_article'),
    path('change-password/', views.change_password, name='change_password'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]