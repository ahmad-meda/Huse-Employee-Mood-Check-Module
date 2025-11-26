from typing import List, Tuple, Optional
from services.service import EmployeeService

class EmployeeProxy:

    @staticmethod
    def get_employee_record(contact_number: str):
        from app import app, db
        with app.app_context():
            return EmployeeService.get_employee_record(contact_number, db.session)
        

   