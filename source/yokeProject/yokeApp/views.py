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
from decimal import Decimal

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

# this view is our about page and shouldn't mess with anything else
class AboutPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/about.html', {})

# this view corresponds to the 'login' endpoint
class LoginPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/login.html', {})

# this view corresponds to the 'account_info' endpoint
class AccountInfo(View):

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        user_info = (User.objects.filter(id=user_id))[0]
        user_data = (UserData.objects.filter(user_id=user_id))[0]
        first_name = user_info.first_name
        last_name = user_info.last_name
        username = user_info.username
        account_balance = user_data.account_balance
        decimal_amount = ((str(account_balance)).split('.'))[1]
        return render(request, 'yokeapp/account_details.html', {"first_name": first_name,
                                                                "last_name": last_name,
                                                                "username": username,
                                                                "account_balance": f'{account_balance:,}'})

# this view corresponds to the 'explore_tasks' endpoint and returns a page with all currently unassigned tasks
class ExploreTasksPage(View):

    def get(self, request, page_number=1, *args, **kwargs):

        # get all unassigned tasks
        unassigned_tasks = Task.objects.filter(queued_by_user_id=None, completed_by_user_id=None)

        return render(request, 'yokeapp/explore_tasks.html', {"unassigned_tasks": unassigned_tasks})

class AddFunds(View):

    def post(self, request, *args, **kwargs):
        # cast QueryDict from form to python dict
        funds_info = request.POST.dict()
        user_id = request.user.id
        user_data = UserData.objects.filter(user_id=user_id)[0]
        print("found user_data: {}".format(user_data))
        amount = Decimal(funds_info["fundsAmount"])
        user_data.account_balance = user_data.account_balance + amount
        user_data.save()

        return redirect('/account_info')


# this view corresponds to the 'create_task' endpoint and contains logic for creating tasks
class CreateTaskPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yokeapp/create_task.html', {})

    def post(self, request, *args, **kwargs):
        # cast QueryDict from form to python dict
        task_info = request.POST.dict()
        created_by_username = UserData.objects.filter(user_id=request.user.id)[0].username
        # create new task in database
        task = Task.objects.create(created_by_user_id=request.user.id,
                                   created_by_username=created_by_username,
                                   task_title=task_info["taskTitle"],
                                   task_description=task_info["taskDescription"],
                                   task_address=task_info["taskAddress"],
                                   task_phone=task_info["taskPhone"],
                                   task_email=task_info["taskEmail"],
                                   task_cost=float(task_info["taskPrice"]),
                                   task_due_date=task_info["taskDueDate"],
                                   estimated_difficulty=task_info["taskDifficulty"])

        return redirect('home/posted/')

# this view corresponds to the 'queue_task/<str:task_id>/' endpoint and contains logic for queueing tasks
class QueueTask(View):

    def get(self, request, task_id, *args, **kwargs):

        # ensure we have a task id
        if task_id is None:
            pass
        else:
            # get the task to queue
            target_task = (Task.objects.filter(task_id=task_id))[0]

            # queue it for that user
            if target_task.queued_by_user_id is None:
                target_task.queued_by_user_id = request.user.id
                queued_by_username = UserData.objects.filter(user_id=request.user.id)[0].username
                target_task.queued_by_username = queued_by_username
                target_task.save()

        # send user back to explore page
        return redirect('/explore_tasks')

# this view corresponds to the 'dequeue_task/<str:task_id>/' endpoint and contains logic for dequeueing tasks
class DeQueueTask(View):

    def get(self, request, task_id, *args, **kwargs):

        # ensure we have a task id
        if task_id is None:
            pass
        else:
            # get task to dequeue
            target_task = (Task.objects.filter(task_id=task_id))[0]
            # dequeue it for all users
            target_task.queued_by_user_id = None
            target_task.queued_by_username = None
            target_task.save()

        # send user back to accepted tasks homepage
        return redirect('/home/accepted')

# this view corresponds to the 'delete_task/<str:task_id>/' endpoint and contains logic for marking tasks as deleted
class DeleteTask(View):

    def get(self, request, task_id, *args, **kwargs):

        # ensure we have a task id
        if task_id is None:
            pass
        else:
            # get task to delete
            target_task = (Task.objects.filter(task_id=task_id))[0]
            # find out how much this task was worth
            task_cost = target_task.task_cost
            # get the ids of the user paying and user to be paid
            user_id_to_pay = target_task.completed_by_user_id
            paying_user_id = target_task.created_by_user_id
            # get the user objects from ids
            owed_user = UserData.objects.filter(user_id=user_id_to_pay)[0]
            paying_user = UserData.objects.filter(user_id=paying_user_id)[0]
            # make the transaction
            paying_user.account_balance -= task_cost
            paying_user.save()
            owed_user.account_balance += task_cost
            owed_user.save()
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
            # get the data for the request user
            userData = UserData.objects.filter(user_id=request.user.id)[0]
            # get the task to complete
            target_task = (Task.objects.filter(task_id=task_id))[0]
            # set its progress to complete
            target_task.task_progress = 1
            # set the completed by user id
            target_task.completed_by_user_id = userData.user_id
            target_task.completed_by_username = userData.username
            # dequeue it for all users
            target_task.queued_by_user_id = None
            target_task.queued_by_username = None
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
                                            user_id=user.id,
                                            first_name=user_info["first_name"],
                                            last_name=user_info["first_name"],
                                            email=user_info["email"])

        # send user back to login page
        response = redirect('/accounts/login')
        return response
