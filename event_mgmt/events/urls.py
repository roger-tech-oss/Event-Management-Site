# events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_user, name='register_user'),
    path('create/', views.create_event, name='create_event'),
    path('event/<int:event_id>/register/', views.register_for_event, name='register'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('rsvp/<int:event_id>/', views.rsvp_event, name='rsvp_event'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('events/details/<int:event_id>/', views.event_detail_json, name='event_detail_json'),
    path('event/<int:event_id>/checkout/', views.checkout, name='checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),
]

    