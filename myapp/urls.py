from django.urls import path
from . import views
from .views import VerificationView
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('register', views.register, name="register"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activation" ),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('counter', views.counter, name='counter'),
    path('activation_success', views.activation_success, name="activation_success"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'), 
    path('auto',views.auto_call, name='auto'),
    path('stop_auto',views.stop_auto, name='stop_auto'),
    path('clear_annual_set',views.clear_annual_set, name='clear_annual_set'),
    path('analysis', views.analysis, name='analysis'),
    path('show_positions_analysis', views.show_positions_analysis, name='show_positions_analysis'),
    path('show_temp_var', views.show_temp_var, name='show_temp_var')
    ]