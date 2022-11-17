from django.urls import path
from . import views


urlpatterns = [
    path('layout/', views.layout, name='layout'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.search, name='search'),
    path('result/', views.result, name='result'),
    path('timetable/', views.timetable, name='timetable'),
    path('details/', views.details, name='details'),
    path('otp/', views.otp, name='otp'),
    path('review/', views.review, name='review'),
    path('history/', views.history, name='history'),
    path('change_pwd/', views.change_pwd, name='change_pwd'),
    path('forgot_pwd/', views.forgot_pwd, name='forgot_pwd'),

]
