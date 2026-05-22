# myapp/urls.py

from django.urls import path
from . import views


urlpatterns = [

   

    path(
        '',
        views.home,
        name='home'
    ),


    

    path(
        'about/',
        views.about,
        name='about'
    ),


    

    path(
        'signup/',
        views.signup_page,
        name='signup'
    ),

    path(
        'login/',
        views.login_page,
        name='login'
    ),

    path(
        'logout/',
        views.logout_page,
        name='logout'
    ),


    

    path(
        'student-dashboard/',
        views.student_dashboard,
        name='student_dashboard'
    ),

    path(
        'my-downloads/',
        views.my_downloads,
        name='my_downloads'
    ),

    path(
        'notifications/',
        views.notifications,
        name='notifications'
    ),


    

    path(
        'teacher-dashboard/',
        views.teacher_dashboard,
        name='teacher_dashboard'
    ),

    path(
        'my-upload/',
        views.my_upload,
        name='my_upload'
    ),


    

    path(
        'notes-list/',
        views.notes_list,
        name='notes_list'
    ),

    path(
        'download-note/<int:note_id>/',
        views.download_note,
        name='download_note'
    ),


    

    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    path(
        'update-profile/',
        views.update_profile,
        name='update_profile'
    ),


    

    path(
        'contact/',
        views.contact,
        name='contact'
    ),


    

    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),
    

path(
    'ask-question/<int:note_id>/',
    views.ask_question,
    name='ask_question'
)

]
