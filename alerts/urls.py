from django.urls import path
from .views import home, map_view, alert_list, user_preferences_view, register

urlpatterns = [
    path('', home, name = 'home'),
    path('map/', map_view, name='map_view'),
    path('alerts/', alert_list, name='alert_list'),
    path('register/', register, name='register'),
    path('preferences/', user_preferences_view, name='user_preferences'),
]