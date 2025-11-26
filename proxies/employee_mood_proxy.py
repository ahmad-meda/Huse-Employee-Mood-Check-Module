from services.employee_mood_service import EmployeeMoodService

class EmployeeMoodProxy:
    @staticmethod
    def get_mood_check_statistics(company_ids=None, group_id=None, start_date=None, end_date=None):
        from app import app, db
        with app.app_context():
            return EmployeeMoodService.get_mood_check_statistics(db.session, company_ids, group_id, start_date, end_date)