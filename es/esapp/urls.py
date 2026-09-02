from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("ex", views.ex, name="ex"),
    path("events", views.events, name="events"),
    path("event-detail/<int:pk>",views.EventDetailView.as_view(), name="event-detail" ),
    path("create", views.create.as_view(), name="create"),
    # simple version of Auth
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("manage", views.manage_events, name="manageE"),
    path("events/edit/<int:id>/", views.event_edit, name="event_edit"),
    path("events/delete/<int:id>/", views.event_delete, name="event_delete"),
    path("my-registrations/", views.my_registrations, name="my_registrations"),
    path(
        "cancel-registration/<int:event_id>/",
        views.cancel_registration,
        name="cancel_registration"
    ),
# API for globals
    path('eventslist/', views.event_list_view, name='event_list_view'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/delete/<int:id>/', views.event_delete, name='event_delete'),
    
    # API TEST endpoints
    path('api/events/',views.api_event_list, name='api_event_list'),
    path('api/events/create/', views.api_event_create, name='api_event_create'),
    path('api/events/delete/<int:id>/', views.api_event_delete, name='api_event_delete'),
]

