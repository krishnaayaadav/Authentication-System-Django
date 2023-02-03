from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Blog

class SignupForm2(forms.ModelForm):
    class Meta:
        model  = User
        fields = ('email', 'username', 'password',)

class SignupForm(UserCreationForm):
    password1 = forms.CharField(label='Password',error_messages={'required': 'Password is required'},  widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password here..'}))
    password2 = forms.CharField(label='Confirm Password', error_messages={'required': 'Confirm Password is required'}, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Re-enter same password here..'}))
    email     = forms.CharField(required=True, error_messages={'required': 'Email id is required'}, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email id here..'}))
    first_name= forms.CharField(required=True, error_messages={'required': 'First Name is required'}, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name here..'}))
    last_name = forms.CharField(required=True, error_messages={'required': 'Last Name is required'}, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name here..'}))


    
    class Meta: 
        model  = User
        fields = ['username','email', 'first_name','last_name']
        
        # custom error messages
        error_messages = {
            'username': {'required': 'Username is required'}
        }

        # custom widgets
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username here..'})
        }


class LoginForm(AuthenticationForm):
    username  = forms.CharField(error_messages={'required': 'Username is required'}, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username here..'}))
    password = forms.CharField(error_messages={'required': 'Password is required'},  widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password here..'}))


class ContactForm(forms.Form):
    name    = forms.CharField(max_length=20)
    subject = forms.CharField(max_length=250)
    sender_email    = forms.EmailField()
    comments         = forms.CharField(widget=forms.Textarea())


class BlogForm(forms.ModelForm):
    class Meta:
        model  = Blog 
        fields = ('title', 'desc')