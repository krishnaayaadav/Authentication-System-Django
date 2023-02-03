from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required

# custom forms here for Authentication
from .forms import SignupForm,LoginForm,ContactForm, BlogForm, SignupForm2
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.hashers import make_password, check_password
from .models import Blog
# Views for Authentication

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

## Here just checking permissions 
# @permission_required('accounts_app.delete_blog')  # checking permission custom using  auth decorator

def home_page(request):
    # print(request.user.has_perm('auth.view_user'))
    # if request.user.has_perm('accounts_app.view_blog'):
    all_blogs = Blog.objects.all()

    password = make_password('krishna23')
    is_same = check_password('krishna23', password)
    print('password is:', is_same)
    response =  render(request,'accounts/home.html',{'all_blogs': all_blogs})

    response.set_cookie('name', 'krishna',domain='127.0.0.1')
    response.set_cookie('lnaklme', 'skldfkkgjkjds',secure=True , max_age=450000)
    return response
    
    # else:
    #     return HttpResponse('You don"t have any permission to view blogs')

def signup_view(request):
    """This view will register new user to our system"""
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm2(request.POST)
            if form.is_valid():
                uemail = form.cleaned_data['email']
                user = form.save()
                activateEmail(request=request, user=user, to_email=uemail)

                # specific groupt ok
                group = Group.objects.get(name = 'Author')

                # defualt user into that select/fetched group
                user.groups.add(group)
                
                messages.success(request, 'Congrats! Account Created Successfuly')
                return redirect('login')
            
        else:
            form = SignupForm2()
        return render(request, 'accounts/signup.html', {'form': form})
    else:
        return redirect('dashboard')

# login view
def login_view(request):
    request_obj = request.COOKIES  #getting all cookies

    if 'name' in  request_obj:
        request_obj['name'] = 'Krishna yadav'
        print(request_obj)
    
    """This view will enable user to login into their account"""
    if not request.user.is_authenticated: 
        try: 

            if request.method == 'POST':
                form = LoginForm(request=request,data = request.POST)
                if form.is_valid():
                    uname = form.cleaned_data['username']
                    upass = form.cleaned_data['password']
                    user = authenticate(username=uname, password=upass)
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'Congrats! Your succeefuly logged in')
                        return redirect('dashboard')
        
            else:
                form = LoginForm()
            response =  render(request, 'accounts/login.html',{'form': form})
            # deleting the cookie
            # response.delete_cookie('name')  
            response.delete_cookie('lname')
            response.delete_cookie('lnaklme')
            return response
        except:
            return HttpResponse('having some Exception')
    else:
        return redirect('dashbaord')

# dashboard view
def dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/dashboard.html')
    else:
        return redirect('login')

# user logout view dashboard_view
def logout_view(request):
    """Logout view here for authenticated users"""
    if request.user.is_authenticated:

        try:
            logout(request)
            messages.success(request, 'You have succssfuly logged out from your account')
            return redirect('login')
        except:
            return HttpResponse('Having some ERROR')
    else:
        return redirect('login')

#Change password using old password
def change_password_view(request):
    """This will use to change user password using previous password"""
    if request.user.is_authenticated:
        user = request.user
        print(user)
        if request.method == 'POST':
            form = PasswordChangeForm(user=user,data = request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Congrats! your password changed successfuly!')
                return redirect('login')
            
        else:
            form = PasswordChangeForm(user=user)
        return render(request, 'accounts/change_password.html',{'form': form})
    else:
        return redirect('login')


# contact form view
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subj = form.cleaned_data['subject']
            user = form.cleaned_data['name']
            email = form.cleaned_data['sender_email']
            message = form.cleaned_data['comments']

            send_mail(subject=subj, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list= [email,])
            print('\n email is send successfuly\n ')
            return redirect('dashbord')
        

    else:
        form = ContactForm()
    return render(request, 'accounts/contact_form.html',{'form': form})
  

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    context = {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
             }
    message = render_to_string('accounts/activate_account.html', context)
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('homepage')