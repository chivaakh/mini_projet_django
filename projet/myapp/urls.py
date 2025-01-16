from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Page de connexion par défaut
    path('home/', views.home, name='home'),  # Page d'accueil après connexion
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('books/', views.list_books, name='list_books'),
]
