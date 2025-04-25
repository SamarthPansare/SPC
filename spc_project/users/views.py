# users/views.py
from audioop import reverse
from base64 import urlsafe_b64decode
import csv
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.shortcuts import get_object_or_404, render, redirect
from users.forms import CustomLoginForm, CustomPasswordResetForm, CustomUserChangeForm, CustomUserUpdateForm, DocumentUpdateForm, PasswordChangeForm, StudentRegistrationForm, UpdateNonTeachingStaffProfileForm, UpdateStudentProfileForm, UpdateTeacherProfileForm, UploadFileForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Import messages framework for debugging
from documents.models import Department, Document, DocumentType
from users.models import CustomUser, Role, UsersNonTeachingStaff, UsersStudent, UsersTeacher
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse


def custom_login(request):
    form = CustomLoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None :
                login(request, user)
                # return redirect('/student')
                # Add more user-type redirections as needed
            
                if user.user_type == "student":
                    return redirect('/student/')
                
                elif user.user_type == "teacher":
                    return redirect('/teacher/')
                
                elif user.user_type == "non_teaching_staff":
                    return redirect('/non-teaching-staff/')
                                
                else:
                    messages.error(request, 'User type isnt assigned')  # Debugging message
                    return redirect('/login')

            else:
                messages.error(request, 'Invalid credentials.')
        else:
            messages.error(request, 'Please provide all required fields.')
    
    return render(request, 'login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('forgot-password')

        # Generate password reset token
        token = default_token_generator.make_token(user)

        # Send email with password reset link
        reset_link = request.build_absolute_uri(reverse('reset-password', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': token}))
        subject = 'Password Reset'
        message = render_to_string('password_reset_email.html', {'reset_link': reset_link})
        send_mail(subject, message, 'samarth.pansare2002@gmail.com', [email])

        messages.success(request, 'Password reset link has been sent to your email.')
        return redirect('login')
    return render(request, 'forgot_password.html')

def reset_password(request, uidb64, token):
    # Handle password reset form submission
    if request.method == 'POST':
        uid = urlsafe_b64decode(uidb64).decode()
        user = get_object_or_404(CustomUser, pk=uid)
        if default_token_generator.check_token(user, token):
            form = CustomPasswordResetForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid or expired password reset link.')
            return redirect('login')
    # Display password reset form
    else:
        form = CustomPasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})



@login_required
def student_dashboard(request):
    # Logic for student dashboard view
    common_features = {
        'View Documents': {'description':'You can view documents uploaded you.', 'url':'student-view-documents'},
        'Upload Documents': { 'description': 'You can upload your documents.', 'url': 'student-upload-documents'}
    }
    user = request.user

    context = {
        'common_features': common_features,
        'user': user
    }
    return render(request, 'student_dashboard.html',context)


@login_required
def teacher_dashboard(request):
    # Logic for teacher dashboard view
    common_features = {
        'View Documents': {'description' : 'You can view documents uploaded by students.', 'url' : 'teacher-view-documents'},
        'Upload Documents': {'description' : 'You can upload documents for students.', 'url' : 'teacher-upload-documents'},
        'View Students': {'description' : 'You can view all students in your class.', 'url' : 'teacher-view-students'},
        'Add Student': {'description' : 'You can add a new student user.', 'url' : 'teacher-add-student'},
        'Add Multiple Student': {'description' : 'You can add multiple students users.', 'url' : 'teacher-add-multiple-students'},
    }
    user = request.user
    teacher_profile = user.teacher_profile
    roles = teacher_profile.roles.all()
    role_features = {}
    for role in roles:
        if role.name == 'teacher':
            continue
        description = 'Access features of ' + role.name + ' from here.'
        url = role.name
        role_features[role.name.title()] = {'description': description, 'url': url}
        
    context = {
        'common_features': common_features,
        'role_features': role_features,
        'user': user,
    }
    return render(request, 'teacher_dashboard.html', context)


@login_required
def non_teaching_staff_dashboard(request):
    # Logic for teacher dashboard view
    # Logic for teacher dashboard view
    common_features = {
        'View Documents': {'description' : 'You can view documents uploaded by students.', 'url' : 'teacher-view-documents'},
        'Upload Documents': {'description' : 'You can upload documents for students.', 'url' : 'teacher-upload-documents'},
        'View Students': {'description' : 'You can view all students in your class.', 'url' : 'teacher-view-students'},
    }
    user = request.user
    context = {
        'common_features': common_features,
        'user': user,
    }
    return render(request, 'non_teaching_staff_dashboard.html',context)


@login_required
def view_profile(request):
    user = request.user
    if user.user_type == 'student':
        student_profile = UsersStudent.objects.get(user=user)
        # Fetch student-specific data
        fields = UsersStudent._meta.get_fields()
        user_data = {field.verbose_name: getattr(student_profile, field.name) for field in fields}
        context = {
            'user': user,
            'user_profile': student_profile,
            'fields' : fields,
            'user_data' : user_data
        }
    elif user.user_type == 'teacher':
        teacher_profile = UsersTeacher.objects.get(user=user)
        # Fetch teacher-specific data
        fields = UsersTeacher._meta.get_fields()

        user_data = {field.verbose_name: getattr(teacher_profile, field.name) for field in fields}
        
        context = {
            'user': user,
            'user_profile': teacher_profile,
            'fields' : fields,
            'user_data' : user_data
        }
    elif user.user_type == 'non_teaching_staff':
        non_teaching_staff_profile = UsersNonTeachingStaff.objects.get(user=user)
        # Fetch non-teaching staff-specific data
        fields = UsersNonTeachingStaff._meta.get_fields()
        user_data = {field.verbose_name: getattr(non_teaching_staff_profile, field.name) for field in fields}
        context = {
            'user': user,
            'user_profile': non_teaching_staff_profile,
            'fields' : fields,
            'user_data' : user_data
        }
    # Add other user types as needed
    
    return render(request, 'view_profile.html', context)


@login_required
def update_profile(request):
    user = request.user
    if user.user_type == 'student':
        student_profile = user.student_profile
        user_form = CustomUserUpdateForm(request.POST or None, instance=user)
        student_form = UpdateStudentProfileForm(request.POST or None, instance=student_profile)

        if request.method == 'POST':
            if user_form.is_valid() and student_form.is_valid():
                user_form.save()
                student_form.save()
                update_session_auth_hash(request, user)  # Update session with new user details
                return redirect('view-profile')  # Redirect to the profile view after updating

        return render(request, 'update_profile.html', {'user_form': user_form, 'student_form': student_form})
    
    elif user.user_type == 'teacher':
        teacher_profile = user.teacher_profile
        user_form = CustomUserUpdateForm(request.POST or None, instance=user)
        teacher_form = UpdateTeacherProfileForm(request.POST or None, instance=teacher_profile)

        if request.method == 'POST':
            if user_form.is_valid() and teacher_form.is_valid():
                user_form.save()
                teacher_form.save()
                update_session_auth_hash(request, user)  # Update session with new user details
                return redirect('view-profile')  # Redirect to the profile view after updating

        return render(request, 'update_profile.html', {'user_form': user_form, 'teacher_form': teacher_form})
    
    elif user.user_type == 'non_teaching_staff':
        non_teaching_staff_profile = user.non_teaching_staff_profile
        user_form = CustomUserUpdateForm(request.POST or None, instance=user)
        non_teaching_staff_form = UpdateNonTeachingStaffProfileForm(request.POST or None, instance=non_teaching_staff_profile)

        if request.method == 'POST':
            if user_form.is_valid() and non_teaching_staff_form.is_valid():
                user_form.save()
                non_teaching_staff_form.save()
                update_session_auth_hash(request, user)  # Update session with new user details
                return redirect('view-profile')  # Redirect to the profile view after updating

        return render(request, 'update_profile.html', {'user_form': user_form, 'non_teaching_staff_form': non_teaching_staff_form})


@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Update the session to prevent the user from being logged out
            messages.success(request, 'Your password was successfully updated!')
            return redirect('custom_login')  # Redirect to the change password page after changing the password
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'password_form': password_form})


@login_required
def student_view_documents(request):
    user = request.user
    docs = Document.objects.filter(owner_id=user.id)
    return render(request, 'view_student_documents.html', {'docs': docs})


@login_required
def student_upload_documents(request):
    if request.method == "POST":
        user = request.user
        student_profile = user.student_profile
        dept = student_profile.department.id
        email = user.email
        user_id = user.id
        docType = int(request.POST.get('docType'))
        name = request.POST.get('name')
        file = request.FILES.get('file')
    
        document = Document(department_id = dept, documentType_id = docType,name = name, file = file, owner_email = email, owner_id=user_id)
        document.save()
        messages.success(request, "Document Added Successfully.")

    docTypes = DocumentType.objects.filter(documentCategory__name__in=['Placements', 'Extracurricular'])

    context = {
        'docTypes' : docTypes
    }

    return render(request, 'upload_student_document.html', context)


@login_required
def teacher_view_documents(request):
    
    user = request.user
    teacher_profile = user.teacher_profile
    department = teacher_profile.department
    docs = department.document_set.all()
    my_docs = Document.objects.filter(owner_id=user.id)
    return render(request, 'view_teacher_documents.html', {'docs': docs, 'my_docs': my_docs, 'dept': department})


@login_required
def teacher_upload_documents(request):
    if request.method == "POST":
        user = request.user
        teacher_profile = user.teacher_profile
        dept_id = teacher_profile.department.id
        user_id = user.id
        email = user.email
        
        doc_type_id = int(request.POST.get('docType'))
        name = request.POST.get('name')
        file = request.FILES.get('file')
    
        document = Document(
            department_id=dept_id,
            documentType_id=doc_type_id,
            name=name,
            file=file,
            owner_email=email,
            owner_id=user_id  # Assign owner_id with the current user's ID
        )
        document.save()
        messages.success(request, "Document Added Successfully.")

    docTypes = DocumentType.objects.all() #getting all possible doctypes
    context = {
        'docTypes' : docTypes
    }

    return render(request, 'upload_teacher_document.html', context)


@login_required
def teacher_view_students(request):
    # Assuming the logged-in user is a teacher
    teacher = request.user.teacher_profile  # Assuming you have a OneToOneField relationship between teacher and user

    # Retrieve all student users belonging to the same department as the teacher
    students = UsersStudent.objects.filter(department=teacher.department)

    return render(request, 'teacher_view_students.html', {'students': students, 'teacher':teacher})


@login_required
def teacher_add_student(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        student_form = StudentRegistrationForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            # Save user
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.user_type = 'student'
            user.save()

            # Save student user
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            # Redirect to a success page or any other desired URL
            return redirect('/teacher-create-student')
    else:
        user_form = UserRegistrationForm()
        student_form = StudentRegistrationForm()

    return render(request, 'create_student_user.html', {'user_form': user_form, 'student_form': student_form})


@login_required
def teacher_add_multiple_students(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            # Assuming CSV file is uploaded
            if uploaded_file.name.endswith('.csv'):
                try:
                    decoded_file = uploaded_file.read().decode('utf-8').splitlines()
                    reader = csv.reader(decoded_file)
                    next(reader, None)  # Skip header row if present
                    for row in reader:
                        # Assuming CSV format: PRN, Department, Class, Division, Batch Year, First Name, Last Name, Username, Password
                        first_name, last_name, user_email, username, prn, department_name, student_class, student_div, batch_year = row
                        password = prn
                        # Retrieve department based on name
                        print(row)
                        department = Department.objects.get(name=department_name)
                        if CustomUser.objects.filter(username=username).exists():
                            continue
                        # Create user and student user
                        user = get_user_model().objects.create_user(
                            username=username, 
                            password=password,
                            email=user_email, 
                            first_name=first_name, 
                            last_name=last_name
                        )
                        student = UsersStudent.objects.create(
                            PRN=prn,
                            department=department,
                            student_class=student_class,
                            student_div=student_div,
                            batch_year=batch_year,
                            user=user
                        )
                
                    messages.success(request, 'Students created successfully.')
                    return redirect('teacher-dashboard')
                except Exception as e:
                    messages.error(request, f'Error processing file: {e}')
            else:
                messages.error(request, 'Unsupported file format. Please upload a CSV file.')
        else:
            messages.error(request, 'Invalid form data.')
    else:
        form = UploadFileForm()
    return render(request, 'teacher_add_multiple_students.html', {'form': form})




@login_required
def update_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST' and 'form_submit' in request.POST:
        form = DocumentUpdateForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document updated successfully.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to previous page or homepage
    else:
        form = DocumentUpdateForm(instance=document)
    return render(request, 'update_document.html', {'form': form, 'document': document})


@login_required
def delete_document_confirmation(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    return render(request, 'delete_document_confirmation.html', {'document': document})


@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully.')
        return redirect('teacher-view-documents')

    return render(request, 'delete_document.html', {'document': document})


# Views based on Roles

def principal(request):
    user = request.user
    user.is_superuser = True
    user.save()
    teacher_profile = user.teacher_profile
    return redirect('/admin/')

def HOD(request):
    pass

def update_student(request, student_id):
    user = get_user_model().objects.get(id=student_id)
    student_profile = user.student_profile

    user_form = CustomUserUpdateForm(request.POST or None, instance=user)
    student_form = UpdateStudentProfileForm(request.POST or None, instance=student_profile)

    if request.method == 'POST' and ('user_form_submit' in request.POST or 'student_form_submit' in request.POST):
        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            update_session_auth_hash(request, user)  
            return redirect('teacher-view-students')  

    else:
        # If the request method is GET, create instances of the forms with instance data only
        user_form = CustomUserUpdateForm(instance=user)
        student_form = UpdateStudentProfileForm(instance=student_profile)

    return render(request, 'update_profile.html', {'user_form': user_form, 'student_form': student_form})

