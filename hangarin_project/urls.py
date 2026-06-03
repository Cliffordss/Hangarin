"""
URL configuration for hangarin_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from tasks import views


admin.site.site_header = "Hangarin Admin"
admin.site.site_title = "Hangarin Admin Portal"
admin.site.index_title = "Welcome to Hangarin Task Manager"


urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    # Redirect old allauth login link back to our local login page
    path('accounts/login/', RedirectView.as_view(pattern_name='login'), name='account_login'),
    path('accounts/signup/', RedirectView.as_view(pattern_name='login'), name='account_signup'),

    # Real Django admin pages
    path('admin/', admin.site.urls),
]