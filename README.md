# cs3450-team8 project: YOKE
For this project our team will be creating a job/task posting platform called YOKE where users will be able to both post jobs and also select jobs to complete. Users who post jobs will be able to pay the users who complete their jobs through the platform, users who complete many jobs can also receive 'karma' style status points as well as good reviews from posters.
# Organization and Name Scheme
### Organization
The organization of this project will be as follows. The root of the github repo will contain the README and two subfolders, 'docs' and 'source'. Docs will contain additional documentation for this project as found useful by the team and required by the assignment. Source will contain the Django API, HTML, and javascript.
### Name Scheme
Python will be the primary backend language for this project so the python naming scheme PEP 8 will be what we use. More info about PEP 8 can be found here: https://www.python.org/dev/peps/pep-0008/

In accordance with this naming scheme we will use the CapWords convention for classes, function names should be lowercase, with words separated by underscores as necessary to improve readability, and filenames should follow the same naming convention as function names.

# Version-control Procedures
We will be using github for version control on this project. This will allow us to track development progress over time and to keep track of each version of the software individually. When a team member goes to create a new feature for the platform, or to fix a bug, they should create a new branch and submit a pull request. Other team members will then review the changes they've made and assuming no corrections are needed they will merge the pull request.
# Tool Stack Description
For this project we are using the following tech stack:

### Version Control
Github
### Backend
On the backend we will use the Django framework and built in webserver
### Frontend 
For the frontend we will use the Bootstrap framework which will be easy to integrate with our Django backend
### Database
We will be using the db.sqlite database that comes with the Django framework
# Tool Stack Setup Procedure
The current working version of Yoke is only a prototype. Requirements to run the project locally:
* ensure python is installed locally on your system
* clone the project repo
* install the required dependancies via the requiremnts.txt file and the following command: "pip install -r requirements.txt"

# Build Instructions
- with the dependancies installed as described above, navigate to the folder containing the "manage.py" file
- once there run the following commands:
- ```python3 manage.py makemigrations yokeApp```
- ```python3 manage.py migrate```
- ```python3 manage.py seed```
- ```python3 manage.py runserver```
# Unit Testing Instructions
For additional testing information please see the YOKE testing document in the docs folder
# System testing instructions
For additional testing information please see the YOKE testing document in the docs folder
