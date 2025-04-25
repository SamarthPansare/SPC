# users/forms.py
from django.contrib.auth.forms import AuthenticationForm
from documents.models import Document
from users.models import CustomUser, UsersNonTeachingStaff, UsersStudent, UsersTeacher
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm

from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class CustomLoginForm(AuthenticationForm):
    # user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)
    pass


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = UsersStudent
        fields = ['PRN', 'department', 'student_class', 'student_div', 'batch_year']  # Add more fields as needed


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name' ,'username', 'email', 'password']  # Add any other required fields for user registration


class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("The two password fields didn't match.")
        return password2


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username']  # Add 'user_type'
        exclude = ['password']

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username']  # Add 'user_type'

class UpdateStudentProfileForm(forms.ModelForm):
    class Meta:
        model = UsersStudent
        fields = ['PRN', 'department', 'student_class', 'student_div', 'batch_year']  # Add more fields as needed

class UpdateTeacherProfileForm(forms.ModelForm):
    class Meta:
        model = UsersTeacher
        fields = ['department', 'roles']  # Add more fields as needed

class UpdateNonTeachingStaffProfileForm(forms.ModelForm):
    class Meta:
        model = UsersNonTeachingStaff
        fields = ['department', 'designation']  # Add more fields as needed


class UploadFileForm(forms.Form):
    file = forms.FileField()


class DocumentUpdateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['owner_email','name', 'file']  # Include fields that can be updated





class CustomPasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def save(self, domain_override=None, subject_template_name='registration/password_reset_subject.txt', email_template_name='registration/password_reset_email.html', use_https=False, token_generator=default_token_generator, from_email=None, request=None, html_email_template_name=None, extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the user.
        """
        email = self.cleaned_data["email"]
        users = self.get_users(email)
        if not users:
            # Run the default password reset form's save method to mimic the behavior
            # of the default PasswordResetForm if no user is found with the given email.
            return super().save(
                domain_override=domain_override,
                subject_template_name=subject_template_name,
                email_template_name=email_template_name,
                use_https=use_https,
                token_generator=token_generator,
                from_email=from_email,
                request=request,
                html_email_template_name=html_email_template_name,
                extra_email_context=extra_email_context,
            )

        # In case the user has both email and phone number fields, you can add logic
        # to check if the provided email exists. If not, check the phone number field.

        # Generate and send reset emails for each user found
        for user in users:
            context = {
                'email': user.email,
                'domain': domain_override,
                'site_name': 'YourSite',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user.email, html_email_template_name=html_email_template_name,
            )

