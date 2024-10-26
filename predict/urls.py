from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),

    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('home/', home, name='home'),

    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('submit/', submit_health_data, name='submit_health_data'),
    path('results/<int:health_data_id>', results, name='results'),
]
