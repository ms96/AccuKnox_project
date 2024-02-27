# Social Networking API 
This is Social Networking Application which can perform basic functionalities such as:
User Login/Signup, Search User, Send/Accept/Reject Friend Request,
List Friends, List Pending Friend Requests.

## Description
This project consist of REST APIs for Social Networking Application. The API's are Authenticated using Django 
Rest Framework Authentication. 
* User Login/Signup
    1. Users can login with their email and password.
    2. User can signup with their email and username.
    3. Except signup and login every api can be called for authenticated users only.
* API to search other users by email and name(paginate up to 10 records per page).
    1. If search keyword matches exact email then return user associated with the email.
    2. If the search keyword contains any part of the name then return a list of all users.
        * i.e. Amarendra, Amar, aman, Abhirama are three users and if users search with "am"
            then all of these users should be shown in the search result because "am"
            substring is part of all of these names.
    3. There will be only one search keyword that will search either by name or email.
* API to send/accept/reject friend request
* API to list friends(list of users who have accepted friend request)
* List pending friend requests(received friend request)
* Users can not send more than 3 friend requests within a minute.

## Techs Used
* Python, Django, Django Rest Framework, SQLite



## Running The Project
1. Clone the project
2. Install Python (if not already installed)
3. Create and activate a virtual environment
4. Install Django (pip install django)
5. Install Django Rest Framework (pip install django djangorestframework)
6. Install any additional dependencies (python3 -m pip install --upgrade pip, pip install django-ratelimit, pip install ...)
7. Run requirements.txt (pip install -r requeriments.txt)
8. Start the development server (python manage.py runserver)



## Usage
1. Register a new user
2. Log in with your credentials
3. Send friend requests to other users
4. Accept/Reject friend requests of other users
5. List Friends(i.e list of users ho have accepted friend request)
6. List pending friend requests(received friend request)

## Postman Collection for the APIS
* Find the **Postman** collection for the apis [Here](https://api.postman.com/collections/3660213-629525d7-a171-4ee6-a5e5-7f2e8d13be9a?access_key=PMAT-01HQP8QFZBPZQGRB77TNFBK9AV)




