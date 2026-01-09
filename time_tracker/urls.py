from django.urls import path
from .views import auth, dashboard, reports, admin_panel, vip, print_views

urlpatterns = [
    path("", auth.home, name="home"),
    path("register/", auth.register_view, name="register"),
    path("login/", auth.login_view, name="login"),
    path("logout/", auth.logout_view, name="logout"),

    path("dashboard/", dashboard.dashboard, name="dashboard"),

    path("reports/", reports.reports_list, name="reports_list"),
    path("reports/new/", reports.report_new, name="report_new"),
    path("reports/<int:report_id>/edit/", reports.report_edit, name="report_edit"),
    path("reports/<int:report_id>/delete/", reports.report_delete, name="report_delete"),

    path("request-vip/", admin_panel.request_vip, name="request_vip"),
    path("request-admin/", admin_panel.request_admin, name="request_admin"),
    path("admin-panel/requests/", admin_panel.admin_requests, name="admin_requests"),
    path("admin-panel/users/", admin_panel.admin_users, name="admin_users"),

    path("vip/export/", vip.vip_export, name="vip_export"),
    path("vip/import/", vip.vip_import, name="vip_import"),

    path("print/", print_views.print_report, name="print_report"),
]
