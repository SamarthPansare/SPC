# users/managers.py
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for handling student, teacher, and other user creations.
    """

    def create_user(self, username, email=None, password=None, user_type='student', **extra_fields):
        """
        Creates and saves a new user with the given email and password.
        """
        if not username:
            raise ValueError('The username must be set')

        user = self.model(
            username=username,
            email=email,
            user_type=user_type,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Creates and saves a new superuser with the given email and password.
        """
        user = self.create_user(username, email, password, user_type='superuser', **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_student(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a new student user.
        """
        return self.create_user(username, email, password, user_type='student', **extra_fields)

    def create_teacher(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a new teacher user.
        """
        return self.create_user(username, email, password, user_type='teacher', **extra_fields)

    # Add methods for creating other user types as needed

