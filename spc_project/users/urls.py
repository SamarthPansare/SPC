from django.urls import path

from users.models import Role
from .views import HOD, change_password, custom_login, custom_logout, delete_document, delete_document_confirmation, department_data, event_co_ordinator, exam, forgot_password, iquac, non_teaching_staff_dashboard, principal, reset_password, staff_add_multiple_students, staff_add_student, staff_upload_documents, staff_view_documents, staff_view_students, student_dashboard, student_view_documents, student_view_syllabus, teacher_add_multiple_students, teacher_add_student, teacher_dashboard, teacher_view_students, student_upload_documents, teacher_view_documents, teacher_upload_documents, update_document, update_profile, update_staff, update_student, update_teacher, vice_principal, view_profile

urlpatterns = [
    path('', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset-password'),

    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    # Dashboards
    path('student/', student_dashboard, name='student-dashboard'),
    path('non-teaching-staff/', non_teaching_staff_dashboard, name='non-teaching-staff-dashboard'),
    path('teacher/', teacher_dashboard, name='teacher-dashboard'),

    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    # Student Urls
    path('student-view-documents', student_view_documents, name='student-view-documents'),
    path('student-upload-documents', student_upload_documents, name='student-upload-documents'),
    path('student-view-syllabus', student_view_syllabus, name='student-view-syllabus'),

    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    # Teacher Urls
    path('teacher-view-documents', teacher_view_documents, name='teacher-view-documents'),
    path('teacher-upload-documents', teacher_upload_documents, name='teacher-upload-documents'),
    path('teacher-view-students', teacher_view_students, name='teacher-view-students'),
    path('teacher-add-student', teacher_add_student, name='teacher-add-student'),
    path('teacher-add-multiple-students', teacher_add_multiple_students, name='teacher-add-multiple-students'),

    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    # Non-teaching-staff Urls
    path('staff-view-documents', staff_view_documents, name='staff-view-documents'),
    path('staff-upload-documents', staff_upload_documents, name='staff-upload-documents'),
    path('staff-view-students', staff_view_students, name='staff-view-students'),
    path('staff-add-student', staff_add_student, name='staff-add-student'),
    path('staff-add-multiple-students', staff_add_multiple_students, name='staff-add-multiple-students'),

    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    # General Urls
    path('view-profile', view_profile, name='view-profile'),
    path('update-profile', update_profile, name='update-profile'),
    path('change-password/', change_password, name='change-password'),

    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    # General Documents Urls
    path('documents/<int:document_id>/update/', update_document, name='update-document'),
    path('documents/<int:document_id>/delete/', delete_document_confirmation, name='delete-document-confirmation'),
    path('documents/<int:document_id>/delete/confirm/', delete_document, name='delete-document'),

    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    # User managing urls
    path('students/<int:student_id>/update/', update_student, name='update-student'),
    path('teachers/<int:teacher_id>/update/', update_teacher, name='update-teacher'),
    path('staff/<int:staff_id>/update/', update_staff, name='update-staff'),
    # path('students/<int:student_id>/delete/', delete_document_confirmation, name='student-delete'),

    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    # Role Based urls
    path('principal', principal, name='principal'),
    path('vice_principal', vice_principal, name='vice_principal'),
    path('HOD', HOD, name='hod'),
    path('exam', exam, name='exam'),
    path('event_co_ordinator', event_co_ordinator, name='event_co_ordinator'),
    path('iquac', iquac, name='iquac'),
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    path('department_data/<int:dept_id>/', department_data, name='department_data'),
    # Add URL patterns for other user dashboards as needed
]
