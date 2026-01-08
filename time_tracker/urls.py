from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("reports/", views.reports_list, name="reports_list"),
    path("reports/new/", views.report_new, name="report_new"),
    path("reports/<int:report_id>/edit/", views.report_edit, name="report_edit"),
    path("reports/<int:report_id>/delete/", views.report_delete, name="report_delete"),
]
