from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home/Login page
    path('dashboard/', views.dashboard, name='dashboard'),  # dashboard page
    path('software/', views.software_list, name='software'),
    path('software/create/', views.software_create, name='software_create'),
    path('software/edit/<int:pk>/', views.software_edit, name='software_edit'),
    path('software/delete/<int:pk>/', views.software_delete, name='software_delete'),
    path('<str:product_extension>/download/', views.protected_redirect, name='protected_redirect'),
    path('usermanual/', views.usermanual, name='usermanual'),  # Usermanual page
    path('usermanual/create/', views.usermanual_create, name='usermanual_create'),
    path('usermanual/delete/<int:pk>/', views.usermanual_delete, name='usermanual_delete'),
    path('usermanual/pdf/<int:pk>/', views.generate_pdf, name='generate_pdf'),
    path('pdf-settings/', views.pdf_settings, name='pdf_settings'),
    path('hello/', views.hello_world, name='hello_world'),  # Hello World page
    path('', views.login_view, name='login'),  # Custom login view
    path('dashboard/', views.dashboard, name='dashboard'),  # Redirect after login
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Custom logout view
]

