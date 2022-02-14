from django.db import models
# Create your models here
import uuid
from datetime import datetime


# this is the user_data table model with information about users that corresponds to a single user account
class UserData(models.Model):
    # here we generate a unique UUID for a user
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user_type is an int that tells us whether they are a task poster or task worker.
    # task_poster = 0
    # task_worker = 1
    # this defaults to task worker
    user_type = models.IntegerField(default=1)
    username = models.CharField(max_length=64)
    email = models.CharField(max_length=150)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    account_creation_date = models.DateTimeField(default=datetime.now, blank=True)
    account_deletion_date = models.DateTimeField(default=None, blank=True)
    account_balance = models.IntegerField(default=0)
    user_rating = models.FloatField(null=True, blank=True, default=None)


# this is the task table model with information that corresponds to a single task
class Task(models.Model):
    # here we generate a unique UUID for a task
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by_user_id = UserData.user_id(null=False)
    deleted_by_user_id = UserData.user_id(null=True)
    queued_by_user_id = UserData.user_id(null=True)
    completed_by_user_id = UserData.user_id(null=True)
    task_creation_time = models.DateTimeField(default=datetime.now, blank=True)
    task_deletion_time = models.DateTimeFiled(default=None, blank=True)
    task_cost = models.IntegerField(default=0)
    # Task Progress: 0 = incomplete, 1 = complete.
    task_progress = models.IntegerField(default=0)
    task_due_date = models.DateTimeField(default=None, blank=True)
    # Estimated Difficulty: 1-10 scale for difficulty and/or time cost of tasks
    estimated_difficulty = models.IntegerField(default=0)

# this is the review table model with information that corresponds to a single user
class Review(models.Model):
    about_user_id = UserData.user_id
    subject_line = models.CharField(max_length=150)
    text_body = models.CharField(max_length=1200)
    star_rating = models.IntegerField(default=0)
    about_task_id = Task.task_id

# This is the messages table model with information that corresponds to a single message
class Message(models.Model):
    from_user_id = UserData.user_id
    to_user_id = UserData.user_id
    subject_line = models.CharField(max_length=64)
    text_body = models.CharField(max_length=2000)
    time_sent = models.DateTimeField(default=datetime.now, blank=True)
