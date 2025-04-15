"""
URL configuration for hcon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from home import views
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = " Admin"
admin.site.site_title = " Admin Portal"
admin.site.index_title = "Welcome"

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('admin/', admin.site.urls),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('upload-research/', views.upload_research, name='upload_research'),
    path('research/', views.research_list, name='research_list'),
    path('research/<str:category>/', views.research_list, name='category_research'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('research/<int:research_id>/', views.research_detail, name='research_detail'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('userform/',views.userForm),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
