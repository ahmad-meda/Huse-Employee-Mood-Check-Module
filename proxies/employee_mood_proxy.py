from services.employee_mood_service import EmployeeMoodService
from Files.SQLAlchemyModels import MoodCheck

class EmployeeMoodProxy:
    @staticmethod
    def get_mood_check_statistics(company_ids=None, group_id=None, start_date=None, end_date=None):
        from app import app, db
        with app.app_context():
            return EmployeeMoodService.get_mood_check_statistics(db.session, company_ids, group_id, start_date, end_date)
    
    @staticmethod
    def add_comment_to_mood_record(mood_record: MoodCheck, comment: str):
        """Add or update a comment to a mood check record."""
        from app import app, db
        with app.app_context():
            return EmployeeMoodService.add_comment_to_mood_record(db.session, mood_record, comment)
    
    @staticmethod
    def add_comment_to_mood_record_by_id(mood_id: int, comment: str):
        """Add or update a comment to a mood check record by ID."""
        from app import app, db
        with app.app_context():
            return EmployeeMoodService.add_comment_to_mood_record_by_id(db.session, mood_id, comment)
