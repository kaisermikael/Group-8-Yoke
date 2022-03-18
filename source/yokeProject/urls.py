"""yokeProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from yokeProject.yokeApp.views import LoginPage
from yokeProject.yokeApp.views import CreateTaskPage
from yokeProject.yokeApp.views import CreateAccountPage
from yokeProject.yokeApp.views import HomePage
from yokeProject.yokeApp.views import ExploreTasksPage

app_name = "yokeApp"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', HomePage.as_view()),
    path('home', HomePage.as_view(), name="home"),
    path('home/<str:home_type>/', login_required(HomePage.as_view())),
    path('explore_tasks', ExploreTasksPage.as_view(), name="ExploreTasksPage"),
    path('explore_tasks/<int:page_number>/', ExploreTasksPage.as_view(), name="ExploreTasksPage"),
    path('create_task', login_required(CreateTaskPage.as_view()), name="CreateTaskPage"),
    path('create_account', CreateAccountPage.as_view(), name="CreateAccountPage"),
]
