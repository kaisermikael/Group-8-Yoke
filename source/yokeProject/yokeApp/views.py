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

# this view corresponds to the 'home/<str:home_type>/' and 'home' endpoints, it returns a dynamic homepage
#   displaying posted, completed, queued, etc. tasks specific to a given user
class HomePage(View):

    def get(self, request, home_type=None, *args, **kwargs):
        # flags that mark which dynamic homepage to go to
        posted = False
        accepted = False
        default = False

        if home_type == "posted":
            posted = True
        elif home_type == "accepted":
            accepted = True
        else:
            default = True

        # get tasks for specific user
        incomplete_user_posted_tasks = Task.objects.filter(created_by_user_id=request.user.id, completed_by_user_id=None)
        completed_user_posted_tasks = Task.objects.filter(created_by_user_id=request.user.id, task_progress=1)
        user_accepted_tasks = Task.objects.filter(queued_by_user_id=request.user.id)
        user_completed_tasks = Task.objects.filter(completed_by_user_id=request.user.id)

        return render(request, 'yokeapp/home.html', {"incomplete_user_posted_tasks": incomplete_user_posted_tasks,
                                                     "completed_user_posted_tasks": completed_user_posted_tasks,
                                                     "posted": posted,
                                                     "accepted": accepted,
                                                     "default": default,
                                                     "user_accepted_tasks": user_accepted_tasks,
                                                     "user_completed_tasks": user_completed_tasks})

# this view corresponds to the 'login' endpoint
class LoginPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/login.html', {})

# this view corresponds to the 'explore_tasks' endpoint and returns a page with all currently unassigned tasks
class ExploreTasksPage(View):

    def get(self, request, page_number=1, *args, **kwargs):

        # get all unassigned tasks
        unassigned_tasks = Task.objects.filter(queued_by_user_id=None, completed_by_user_id=None)

        return render(request, 'yokeapp/explore_tasks.html', {"unassigned_tasks": unassigned_tasks})


# this view corresponds to the 'create_task' endpoint and contains logic for creating tasks
class CreateTaskPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/create_task.html', {})

    def post(self, request, *args, **kwargs):
        # cast QueryDict from form to python dict
        task_info = request.POST.dict()
        # create new task in database
        task = Task.objects.create(created_by_user_id=request.user.id,
                                   task_title=task_info["taskTitle"],
                                   task_description=task_info["taskDescription"],
                                   task_cost=float(task_info["taskPrice"]),
                                   task_due_date=task_info["taskDueDate"],
                                   estimated_difficulty=task_info["taskDifficulty"])

        return redirect('home/posted/')

# this view corresponds to the 'queue_task/<str:task_id>/' endpoint and contains logic for queueing tasks
class QueueTask(View):

    def get(self, request, task_id=None, *args, **kwargs):

        # ensure we have a task id
        if task_id is None:
            pass
        else:
            # get the task to queue
            target_task = (Task.objects.filter(task_id=task_id))[0]

            # queue it for that user
            if target_task.queued_by_user_id is None:
                target_task.queued_by_user_id = request.user.id
                target_task.save()

        # send user back to explore page
        return redirect('/explore_tasks')

# this view corresponds to the 'dequeue_task/<str:task_id>/' endpoint and contains logic for dequeueing tasks
class DeQueueTask(View):

    def get(self, request, task_id=None, *args, **kwargs):

        # ensure we have a task id
        if task_id is None:
            pass
        else:
            # get task to dequeue
            target_task = (Task.objects.filter(task_id=task_id))[0]
            # dequeue it for all users
            target_task.queued_by_user_id = None
            target_task.save()

        # send user back to accepted tasks homepage
        return redirect('/home/accepted')

# this view corresponds to the 'delete_task/<str:task_id>/' endpoint and contains logic for marking tasks as deleted
class DeleteTask(View):

    def get(self, request, task_id=None, *args, **kwargs):

        # ensure we have a task id
        if task_id is None:
            pass
        else:
            # get task to delete
            target_task = (Task.objects.filter(task_id=task_id))[0]
            target_task.delete()

        # send user back to posted tasks homepage
        return redirect('/home/posted')

# this view corresponds to the 'complete_task/<str:task_id>/' endpoint and contains logic for marking tasks as complete
class CompleteTask(View):

    def get(self, request, task_id=None, *args, **kwargs):

        # ensure we have a task id
        if task_id is None:
            pass
        else:
            # get the task to complete
            target_task = (Task.objects.filter(task_id=task_id))[0]
            # set its progress to complete
            target_task.task_progress = 1
            # remove it from any users queue
            target_task.queued_by_user_id = None
            # set the completed by user id
            target_task.completed_by_user_id = request.user.id
            # save those changes
            target_task.save()

        # send the user back to their accepted tasks homepage
        return redirect('/home/accepted')


# this view corresponds to the 'create_account' endpoint and contains the logic for creating user accounts
class CreateAccountPage(View):

    def get(self, request, *args, **kwargs):
        # get url query params invalid?=, here data represents what element (ex. username) was invalid
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
            # create new user object
            user = User.objects.create_user(username=(user_info["username"]),
                                            first_name=user_info["first_name"],
                                            last_name=user_info["first_name"],
                                            email=user_info["email"],
                                            password=user_info["password_2"])
        except IntegrityError as e:
            # let the user know that username is taken
            if "auth_user.username" in str(e.args)[0]:
                response = redirect('/create_account?invalid=username')
                return response
            # let the user know that email is taken
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

        # send user back to login page
        response = redirect('/accounts/login')
        return response
