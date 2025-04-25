from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name='home'),    #configuring document view on blank url
    path('stream', views.stream, name='stream'),
    path('department/<int:stream_id>/', views.department, name='department'),
    path('view-all-documents/<int:dept_id>/', views.view_all_documents, name='view_all_documents'), 
    path('add-document', views.add_document, name='add_document'),
]
