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
from django.http import HttpResponseNotFound
    
class HomePage(View):

    def get(self, request, home_type=None, *args, **kwargs):
        posted = False
        accepted = False
        default = False
        # print("got home type: {}".format(home_type))
        if home_type == "posted":
            posted = True
        elif home_type == "accepted":
            accepted = True
        else:
            default = True

        user_posted_tasks = Task.objects.filter(created_by_user_id=request.user.id)
        user_accepted_tasks = Task.objects.filter(queued_by_user_id=request.user.id)

        # print(("posted tasks for user {}:".format(request.user.first_name)))
        return render(request, 'yokeapp/home.html', {"user_posted_tasks": user_posted_tasks,
                                                     "posted": posted,
                                                     "accepted": accepted,
                                                     "default": default,
                                                     "user_accepted_tasks": user_accepted_tasks})


class LoginPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/login.html', {})

class ExploreTasksPage(View):

    def get(self, request, page_number=1, *args, **kwargs):

        unassigned_tasks = Task.objects.filter(queued_by_user_id=None)
        print("Found all unnassigned tasks")
        for x in unassigned_tasks:
            print("Task: {}, assigned to user: {}".format(x.task_title, x.queued_by_user_id))
        return render(request, 'yokeapp/explore_tasks.html', {"unassigned_tasks": unassigned_tasks})


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

        return redirect('home/posted/')


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
