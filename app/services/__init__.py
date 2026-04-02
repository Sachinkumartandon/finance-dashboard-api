from app.services.auth_service import register_user, login_user
from app.services.user_service import get_all_users, get_user_by_id, update_user, delete_user
from app.services.record_service import create_record, get_records, get_record_by_id, update_record, soft_delete_record
from app.services.dashboard_service import get_summary, get_by_category, get_monthly_trends, get_recent_activity
