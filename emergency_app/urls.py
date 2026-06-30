from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
    "report/",
    views.report_emergency,
    name="report_emergency"
),

    path(
    "my-reports/",
    views.my_reports,
    name="my_reports"
),
    path(
    "profile/",
    views.profile,
    name="profile"
),
    path(
    "report/<int:report_id>/",
    views.report_detail,
    name="report_detail"
),
    path(
    "track-dispatch/",
    views.track_dispatch,
    name="track_dispatch"
),
    path(
    "emergency-contacts/",
    views.emergency_contacts,
    name="emergency_contacts"
),
    path(
    "response-guidelines/",
    views.response_guidelines,
    name="response_guidelines"
),
    path(
    "track-dispatch/",
    views.track_dispatch,
    name="track_dispatch"
),
]
