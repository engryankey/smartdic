"""tydictionary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from naijadictionary import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.http import require_http_methods

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('register/', views.userreg, name="userreg"),
    path('login/', views.userlogin, name="userlogin"),
    path('logout/', views.userlogout, name="logout"),
    path('words/', views.WordsListView.as_view(), name="wordslistview"),
    path('words/<slug>/', views.WordDetailView.as_view(), name="worddetailview"),
    # path('words/<slug>/<slug>/', views.Detaildetail.as_view(), name="detaildetail"),
    path('dashboard/', views.UserDashboard.as_view(), name="dashboard"),
    path('dashboard/newword/', views.DefCreateView.as_view(), name="defcreateview"),
    path('dashboard/updateprofile/<int:pk>/', views.DefUpdateView.as_view(), name="updateprofile"),
    # path('words/<int:pk>/', views.WordDetailView.as_view(), name="worddetailview"), this if you need id at the end then link will be .id
    # path('result/', views.result, name="result"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
