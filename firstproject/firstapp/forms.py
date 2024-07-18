from django import forms
from django.core import validators

from .models import appusers, genre, book,chapters,feedback,requestbook
# from django.db import models


class appusersForm(forms.ModelForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'id_username', 'class': 'input-field'}), validators=[validators.RegexValidator(r'^[A-Za-z\s]+$', 'Enter a valid name with alphabets and spaces only.'), validators.MaxLengthValidator(20, 'Name should be maximum 20 characters long.')])
    emailid = forms.CharField(max_length=50, widget=forms.EmailInput(attrs={'id': 'id_emailid', 'class': 'input-field'}),validators=[validators.EmailValidator(message='Enter a valid email address.')])
    phone = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'id': 'id_phone','class':'input-field'}), validators=[validators.RegexValidator(r'^\d+$', 'Enter a valid digit.')])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field'}), validators=[
        validators.MinLengthValidator(8, 'Password should be at least 8 characters long.'),
        validators.RegexValidator(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=]).*$',
            'Password should include at least one uppercase letter, one lowercase letter, one digit, and one special character.'
        )
    ])
    confirmpassword = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'id_confirmpassword','class': 'input-field'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirmpassword')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New password and confirm password must match.")

    class Meta:
        model = appusers
        fields = ['username', 'emailid', 'phone', 'password']


class addgenreForm(forms.ModelForm):
    genrename = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'id_genrename' ,'style':'color:white; border-radius:9px;margin-left:12px;background-color:black;border:2px solid white;'}))

    class Meta:
        model = genre
        fields = ['genrename']

class bookForm(forms.ModelForm):
    genrename = forms.ModelChoiceField(queryset=genre.Objects.all(),empty_label=None,
                widget=forms.Select(attrs={'id':'id_genrename', 'style':'border-radius:5px; background-color:black;color:white;padding:2px;'}))
    title = forms.CharField(max_length=50,
                widget=forms.TextInput(attrs={'id':'id_title','style':'border-radius:5px; background-color:black;color:white;padding:2px;'}))
    author = forms.CharField(max_length=50,
                widget=forms.TextInput(attrs={'id':'id_author','style':'border-radius:5px; background-color:black;color:white;padding:2px;'}))
    bookdesc = forms.CharField(max_length=500,
                widget=forms.Textarea(attrs={'id':'id_bookdesc','style':'border-radius:5px; background-color:black;color:white;padding:2px;'}))
    imagefilename = forms.FileField(
                widget=forms.FileInput(attrs={'id':'id_imagefilename','style':'border-radius:5px; background-color:black;color:white;padding:2px;'}))

    class Meta:
        model = book
        fields = ['genrename','title','author','bookdesc','imagefilename']




class chapterForm(forms.ModelForm):
    #title is a an form field just to display title but not part of chapters model
    title=forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'id_title'}))
    chapterno = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'id': 'id_chapterno'}))
    chapterfilename = forms.FileField(
        widget=forms.FileInput(attrs={'id': 'id_chapterfilename'}))
    class Meta:
        model = chapters
        fields = ['title','chapterno','chapterfilename']

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New password and confirm password must match.")

class AdminChangePasswordForm(forms.Form):
    admincurrent_password = forms.CharField(widget=forms.PasswordInput)
    adminnew_password = forms.CharField(widget=forms.PasswordInput)
    adminconfirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New password and confirm password must match.")


class feedbackForm(forms.ModelForm):
    feedback = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'id':'id_feedback'}))

    class Meta:
        model = feedback
        fields = ['feedback']

class requestForm(forms.ModelForm):
    bookname = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'id':'id_bookname'}))
    bookgenre = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'id':'id_bookgenre'}))
    authorname = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'id':'id_authorname'}))

    class Meta:
        model = requestbook
        fields = ['bookname', 'bookgenre', 'authorname']


