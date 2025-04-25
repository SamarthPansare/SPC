from django.urls import path

from users.models import Role
from .views import HOD, change_password, custom_login, custom_logout, delete_document, delete_document_confirmation, forgot_password, non_teaching_staff_dashboard, principal, reset_password, student_dashboard, student_view_documents, teacher_add_multiple_students, teacher_add_student, teacher_dashboard, teacher_view_students, student_upload_documents, teacher_view_documents, teacher_upload_documents, update_document, update_profile, update_student, view_profile

urlpatterns = [
    path('', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset-password'),

    path('student/', student_dashboard, name='student-dashboard'),
    path('non-teaching-staff/', non_teaching_staff_dashboard, name='non-teaching-staff-dashboard'),
    path('teacher/', teacher_dashboard, name='teacher-dashboard'),

    path('student-view-documents', student_view_documents, name='student-view-documents'),
    path('student-upload-documents', student_upload_documents, name='student-upload-documents'),

    path('teacher-view-documents', teacher_view_documents, name='teacher-view-documents'),
    path('teacher-upload-documents', teacher_upload_documents, name='teacher-upload-documents'),
    path('teacher-view-students', teacher_view_students, name='teacher-view-students'),
    path('teacher-add-student', teacher_add_student, name='teacher-add-student'),
    path('teacher-add-multiple-students', teacher_add_multiple_students, name='teacher-add-multiple-students'),

    path('view-profile', view_profile, name='view-profile'),
    path('update-profile', update_profile, name='update-profile'),
    path('change-password/', change_password, name='change-password'),

    path('documents/<int:document_id>/update/', update_document, name='update-document'),
    path('documents/<int:document_id>/delete/', delete_document_confirmation, name='delete-document-confirmation'),
    path('documents/<int:document_id>/delete/confirm/', delete_document, name='delete-document'),

    path('students/<int:student_id>/update/', update_student, name='update-student'),
    # path('students/<int:student_id>/delete/', delete_document_confirmation, name='student-delete'),

    path('principal', principal, name='principal'),
    path('HOD', HOD, name='HOD'),
    path('assistant-professor', HOD, name='Assistant Professor'),

    # Add URL patterns for other user dashboards as needed
]
