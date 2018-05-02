from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.redirect_to_home, name='redirect_to_home'),
    path('login/', auth_views.LoginView.as_view(template_name="FSJ/login.html", redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.registration, name='register'),
    path('register/password_set/(P<uidb64>[0-9A-Za-z]+)-(P<token>.+)/', views.register_activation, name='register_activation'),
    path('reset_password/', auth_views.password_reset, name='reset_password'),
    path('reset_password/done/', auth_views.password_reset_done, name='password_reset_done'),
    path('reset_password/confirm/(P<uidb64>[0-9A-Za-z]+)-(P<token>.+)/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('reset_password/complete/', auth_views.password_reset_complete, name='password_reset_complete'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('studentlist/', views.coordinator_studentlist, name = 'studentlist'),
    path('studentlist/add/', views.coordinator_addstudent, name = 'addstudent'),
    path('studentlist/addmulti/', views.coordinator_upload_students, name = 'uploadstudent'),
    path('studentlist/delete/', views.coordinator_deletestudent, name = 'deletestudent'),
    path('edit_student', views.edit_student, name = 'edit_student'),
    path('adjudicatorlist/', views.coordinator_adjudicatorlist, name = 'adjudicatorlist'),
    path('adjudicatorlist/add/', views.coordinator_addadjudicator, name = 'addadjudicator'),
    path('adjudicatorlist/delete/', views.coordinator_deleteadjudicator, name = 'deleteadjudicator'),
    path('edit_adjudicator', views.edit_adjudicator, name = 'edit_adjudicator'),
    path('coord_awardslist/', views.awards, name='coord_awardslist'),
    path('coord_awardslist/add/', views.coordinator_add_awards, name = 'coord_addaward'),
    path('coord_awardslist/action/', views.coordinator_awardaction, name='coord_awardaction'),
    path('coord_awardslist/<str:award_idnum>/', views.coordinator_awardedit, name = 'coord_awardedit'),
    path('programs/list_programs/', views.list_programs, name='list_programs'),
    path('programs/add/', views.add_program, name='add_program'),
    path('programs/edit/<str:program_code>/', views.edit_program, name='edit_program'),
    path('programs/delete/', views.delete_programs, name='delete_programs'),
    path('coord_yearslist/', views.years, name='coord_yearslist'),
    path('coord_yearslist/add/', views.coordinator_addyearofstudy, name = 'coord_addyear'),
    path('coord_yearslist/delete/', views.coordinator_yeardelete, name='coord_deleteyear'),
    path('edit_year', views.edit_year, name = 'edit_year'),
    path('coord_committeeslist/', views.committees, name = 'coord_committeeslist'),
    path('coord_committeeslist/add/', views.coordinator_addcommittee, name = 'coord_addcommittee'),
    path('coord_committeeslist/delete/', views.coordinator_committeedelete, name='coord_deletecommittee'),
    path('coord_committeeslist/<str:committee_idnum>/', views.coordinator_committeeedit, name = 'coord_committeeedit'),
    path('coord_awardslist/<str:award_idnum>/applications/', views.coordinator_application_list, name = 'coord_applicationlist'),
    path('coord_awardslist/<str:award_idnum>/applications/archive/view/<str:application_idnum>/', views.coordinator_archived_application_view, name = 'coord_applicationview'),
    path('coord_awardslist/<str:award_idnum>/applications/archive/', views.coordinator_application_archive_list, name = 'coord_application_archive'),
    path('coord_awardslist/<str:award_idnum>/applications/archive/action/', views.coordinator_archive_action, name = 'coord_archive_action'),
    path('coord_awardslist/<str:award_idnum>/applications/action/', views.coordinator_application_action, name = 'coord_application_action'),
    path('student_awardslist/', views.student_awardslist, name = 'student_awardslist'),
    path('student_awardslist/<str:award_idnum>/apply/', views.student_addapplication, name = 'student_addapplication'),
    path('student_awardslist/<str:award_idnum>/edit/', views.student_editapplication, name = 'student_editapplication'),
    path('student_awardslist/<str:award_idnum>/unsubmit/', views.student_unsubmitapplication, name = 'student_unsubmitapplication'),
    path('student_awardslist/<str:award_idnum>/delete/', views.student_deleteapplication, name = 'student_deleteapplication'),
    path('adj_awardslist/', views.adjudicator_awards, name = 'adj_awardslist'),
    path('adj_awardslist/<str:award_idnum>/applications/', views.adjudicator_application_list, name = 'adj_applicationlist'),
    path('adj_awardslist/<str:award_idnum>/<str:application_idnum>/edit/', views.adjudicator_add_edit_comment_ranking, name = 'adj_editcomment'),
    path('adj_awardslist/<str:award_idnum>/<str:application_idnum>/delete/', views.adjudicator_delete_comment, name = 'adj_deletecomment'),
    path('view_student', views.view_student, name = 'view_student'),
    path('view_application', views.view_application, name = 'view_application')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
