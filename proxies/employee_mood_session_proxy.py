from services.employee_mood_session_service import EmployeeMoodSessionService

class EmployeeMoodSessionProxy:
    # Create one instance to use everywhere
    _service = EmployeeMoodSessionService()

    @classmethod
    def set_employee_asked_user_feedback(cls, contact_number, asked_feedback):
        """Set asked user feedback status for an employee"""
        return cls._service.set_employee_asked_user_feedback(contact_number, asked_feedback)
    
    @classmethod
    def get_employee_asked_user_feedback(cls, contact_number):
        """Get asked user feedback status for an employee"""
        return cls._service.get_employee_asked_user_feedback(contact_number)
    
    @classmethod
    def clear_employee_asked_user_feedback(cls, contact_number):
        """Clear asked user feedback status for an employee"""
        return cls._service.clear_employee_asked_user_feedback(contact_number)