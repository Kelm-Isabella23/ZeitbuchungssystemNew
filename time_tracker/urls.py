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

    path("request-vip/", views.request_vip, name="request_vip"),
    path("request-admin/", views.request_admin, name="request_admin"),
    path("admin-panel/requests/", views.admin_requests, name="admin_requests"),
    path("admin-panel/users/", views.admin_users, name="admin_users"),

    path("vip/export/", views.vip_export, name="vip_export"),
    path("vip/import/", views.vip_import, name="vip_import"),
]

