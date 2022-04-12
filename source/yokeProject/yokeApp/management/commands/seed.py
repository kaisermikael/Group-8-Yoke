from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from yokeProject.yokeApp.models import UserData, Task


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write("Creating admin account...")
        # create new user object
        admin_user = User.objects.create_user(username="admin",
                                              first_name="admin",
                                              last_name="admin",
                                              email="admin",
                                              password="admin")
        # create a user_data model object / entry in database
        admin_user_data = UserData.objects.create(username="admin",
                                                  user_id=admin_user.id,
                                                  first_name="admin",
                                                  last_name="admin",
                                                  email="admin")
        self.stdout.write("Done! Username: \'admin\' Password: \'admin\'")

