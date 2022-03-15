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
    username = models.CharField(max_length=64, null=False)
    email = models.CharField(max_length=150, null=False)
    first_name = models.CharField(max_length=64, null=False)
    last_name = models.CharField(max_length=64, null=False)
    password = models.CharField(max_length=64)
    account_creation_date = models.DateTimeField(default=datetime.now, blank=True)
    account_deletion_date = models.DateTimeField(default=None, blank=True, null=True)
    account_balance = models.IntegerField(default=0)
    user_rating = models.FloatField(null=True, blank=True, default=None)


# this is the task table model with information that corresponds to a single task
class Task(models.Model):
    # here we generate a unique UUID for a task
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by_user_id = models.IntegerField(null=True, blank=False)
    deleted_by_user_id = models.IntegerField(blank=True, null=True)
    queued_by_user_id = models.IntegerField(blank=True, null=True)
    completed_by_user_id = models.IntegerField(blank=True, default=0)
    task_title = models.CharField(max_length=64, default="default task title")
    task_description = models.CharField(max_length=300)
    task_creation_time = models.DateTimeField(default=datetime.now, blank=True)
    task_deletion_time = models.DateTimeField(blank=True, null=True)
    task_cost = models.IntegerField(default=0)
    # Task Progress: 0 = incomplete, 1 = complete.
    task_progress = models.IntegerField(default=0)
    task_due_date = models.DateField()
    # Estimated Difficulty: 1-10 scale for difficulty and/or time cost of tasks
    estimated_difficulty = models.IntegerField(default=0)


# this is the review table model with information that corresponds to a single user
class Review(models.Model):
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    about_user_id = models.IntegerField(blank=False, null=True)
    subject_line = models.CharField(max_length=150)
    text_body = models.CharField(max_length=1200)
    star_rating = models.IntegerField(default=0)
    about_task_id = Task.task_id


# This is the messages table model with information that corresponds to a single message
class Message(models.Model):
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user_id = models.IntegerField(blank=False, null=True)
    to_user_id = models.IntegerField(blank=False, null=True)
    subject_line = models.CharField(max_length=64)
    text_body = models.CharField(max_length=2000)
    time_sent = models.DateTimeField(default=datetime.now, blank=True)
