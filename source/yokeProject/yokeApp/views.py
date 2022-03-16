from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth.models import User
from yokeProject.yokeApp.models import UserData, Task
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
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

    def post(self, request, *args, **kwargs):
        user_dict = {"first_name": request.user.first_name, "last_name": request.user.last_name, "id": request.user.id}
        # cast QueryDict from form to python dict
        task_info = request.POST.dict()
        # create new task in database
        task = Task.objects.create(created_by_user_id=request.user.id,
                                   task_title=task_info["taskTitle"],
                                   task_description=task_info["taskDescription"],
                                   task_cost=task_info["taskPrice"],
                                   task_due_date=task_info["taskDueDate"],
                                   estimated_difficulty=task_info["taskDifficulty"])
        # print("got task_info: {}".format(task_info))
        # print("got user: {}".format(user_dict))
        # print("created task: {}".format(task))

        return render(request, 'yokeapp/home_worker.html', {})


class CreateAccountPage(View):

    def get(self, request, *args, **kwargs):
        data = request.GET.get('invalid', '')
        if data != '':
            sorry_message = True
            return render(request, 'yokeapp/create_account.html', {"sorry_message": sorry_message,
                                                                   "info_type": data})
        else:
            return render(request, 'yokeapp/create_account.html', {})

    def post(self, request, *args, **kwargs):
        # cast QueryDict from form to python dict
        user_info = request.POST.dict()
        # create new user in database
        try:
            user = User.objects.create_user(username=(user_info["username"]),
                                            first_name=user_info["first_name"],
                                            last_name=user_info["first_name"],
                                            email=user_info["email"],
                                            password=user_info["password_2"])
        except IntegrityError as e:
            print(str(e.args))
            if "auth_user.username" in str(e.args)[0]:
                response = redirect('/create_account?invalid=username')
                return response
            elif "auth_user.email" in str(e.args)[0]:
                response = redirect('/create_account?invalid=email')
                return response
            else:
                response = redirect('/create_account?invalid=username')
                return response
        # create a user_data model object / entry in database
        user_data = UserData.objects.create(username=(user_info["username"]),
                                            first_name=user_info["first_name"],
                                            last_name=user_info["first_name"],
                                            email=user_info["email"])
        # print("created user_data: {}".format(user_data))
        # print("Created new user: {}".format(user_info))

        response = redirect('/accounts/login')
        return response


class WorkerTaskViewPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/worker_view_task.html', {})
