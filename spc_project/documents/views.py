# documents/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from documents.models import Stream, Department, DocumentType, Document

# Create your views here.

def index(request):
    return redirect('/stream')


def stream(request):
    streams = Stream.objects.all()
    context = {
        'streams' : streams
    }

    if request.method == "POST":
        stream_id = int(request.POST.get('stream'))

        return redirect('department', stream_id)
    
    return render(request, 'streams.html', context)



def department(request, stream_id):
    stream = Stream.objects.get(pk = stream_id)     #getting the stream object from id
    depts = stream.department_set.all()     #getting all the departments from stream

    context = {
        'depts' : depts
    }

    if request.method == "POST":
        dept_id = int(request.POST.get('dept'))
        choice = request.POST.get('choice')
        
        if choice == "view_documents":
            return redirect('view_all_documents', dept_id)
        elif choice == "upload_document":
            return redirect('/add-document')
        
    
    return render(request, 'departments.html', context)


def view_all_documents(request, dept_id):
    
    dept = Department.objects.get(pk = dept_id)
    docs = dept.document_set.all()
    for doc in docs:
        if not doc.file:
            doc.file = None
            
    context = {
        'dept' : dept,
        'docs' : docs
    }
    
    return render(request,'viewDocuments.html', context)



def add_document(request):
    if request.method == "POST":
        dept = int(request.POST.get('dept'))
        docType = int(request.POST.get('docType'))
        name = request.POST.get('name')
        file = request.FILES.get('file')

        document = Document(department_id = dept, documentType_id = docType,name = name, file = file)
        document.save()
        messages.success(request, "Document Added Successfully.")

    # getting streams, depts and docTypes to provide options

    depts = Department.objects.all() #getting all deprtments
    docTypes = DocumentType.objects.all() #getting all possible doctypes

    context = {
        'depts' : depts,
        'docTypes' : docTypes
    }
    
    return render(request, 'uploadDocument.html', context)

