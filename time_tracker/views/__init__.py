default_app_config = "time_tracker.apps.TimeTrackerConfig"

from .auth import home, register_view, login_view, logout_view
from .dashboard import dashboard
from .reports import reports_list, report_new, report_edit, report_delete
from .admin_panel import request_vip, request_admin, admin_requests, admin_users
from .vip import vip_export, vip_import
from .print_views import print_report
