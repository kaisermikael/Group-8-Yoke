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
from yokeProject.yokeApp.views import DeleteTask, LoginPage, CreateTaskPage, CompleteTask, QueueTask, \
    ExploreTasksPage, DeQueueTask, HomePage, CreateAccountPage, AccountInfo, AddFunds

app_name = "yokeApp"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', HomePage.as_view()),
    path('home', HomePage.as_view(), name="home"),
    path('home/<str:home_type>/', login_required(HomePage.as_view())),
    path('explore_tasks', ExploreTasksPage.as_view(), name="ExploreTasksPage"),
    path('account_info', login_required(AccountInfo.as_view()), name="AccountInfo"),
    path('explore_tasks/<int:page_number>/', ExploreTasksPage.as_view(), name="ExploreTasksPage"),
    path('create_task', login_required(CreateTaskPage.as_view()), name="CreateTaskPage"),
    path('add_funds', login_required(AddFunds.as_view()), name='AddFunds'),
    path('queue_task/<str:task_id>/', login_required(QueueTask.as_view()), name="QueueTask"),
    path('dequeue_task/<str:task_id>/', login_required(DeQueueTask.as_view()), name="DeQueueTask"),
    path('delete_task/<str:task_id>/', login_required(DeleteTask.as_view()), name="DeleteTask"),
    path('complete_task/<str:task_id>/', login_required(CompleteTask.as_view()), name="CompleteTask"),
    path('create_account', CreateAccountPage.as_view(), name="CreateAccountPage"),
]
