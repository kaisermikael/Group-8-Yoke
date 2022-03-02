from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from yokeProject.yokeApp.models import UserData
import json


class TaskerHomePage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/home_tasker.html', {})


class WorkerHomePage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/home_worker.html', {})


class LoginPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/login.html', {})


class CreateTaskPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/create_task.html', {})


class CreateAccountPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/create_account.html', {})

    def post(self, request, *args, **kwargs):
        # cast QueryDict from form to python dict
        user_info = request.POST.dict()
        # create new user in database
        user = User.objects.create_user(username=(user_info["username"]),
                                        first_name=user_info["first_name"],
                                        last_name=user_info["first_name"],
                                        email=user_info["email"],
                                        password=user_info["password_2"])
        # create a user_data model object / entry in database
        user_data = UserData.objects.create(username=(user_info["username"]),
                                            first_name=user_info["first_name"],
                                            last_name=user_info["first_name"],
                                            email=user_info["email"])
        print("created user_data: {}".format(user_data))
        print("Created new user: {}".format(user_info))

        return render(request, 'yokeapp/home_worker.html', {})


class WorkerTaskViewPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/worker_view_task.html', {})
