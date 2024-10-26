from django.urls import path

from .views import submit_health_data, index, results

urlpatterns = [
    path('', index, name='index'),
    path('submit/', submit_health_data, name='submit_health_data'),  # Add this line
    path('results/', results, name='results'),  # Add this line
]
