# users/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from documents.models import Department, Stream
from users.managers import CustomUserManager  # Import the Stream and Department model from the documents app


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('non_teaching_staff', 'Non-Teaching Staff'),
        ('vice_principal', 'Vice Principal'),
        ('principal', 'Principal'),
        ('superuser', 'Superuser'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    groups = models.ManyToManyField(Group, related_name='custom_user_groups')  # Change related_name
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')  # Change related_name    
       
    objects = CustomUserManager()  # Set the custom manager
    def __str__(self):
        return self.username


class UsersStudent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    PRN = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    student_class = models.CharField(max_length=20)
    student_div = models.CharField(max_length=20)
    batch_year = models.IntegerField()
    # Add more fields as needed
    def __str__(self):
        return self.user.username

class Role(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class UsersTeacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    roles = models.ManyToManyField(Role)  # Many-to-many relationship with Role model
    # Add more fields as needed

class UsersNonTeachingStaff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='non_teaching_staff_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    designation = models.CharField(max_length=100)
    # Add more fields as needed

