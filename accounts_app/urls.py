from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
      # home page for permission checking
    path('', home_page,name='homepage'),

    path('signup/', signup_view, name='signup'),
    path('activate/',activateEmail),
    path('activate-accounts/<uidb64>/<token>/',activate, name='activate'),
    path('login/', login_view,name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('password/change/', change_password_view, name='change_password'),
    path("contact/",contact_view, name=""),
    

    # password -reset -views here

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='password-resets/password_reset_form.html'), name='password-reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password-resets/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password-resets/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-rest-complet/', auth_views.PasswordResetCompleteView.as_view(template_name='password-resets/password_reset_complete.html'), name='password_reset_complete'),
    

  
   
]
