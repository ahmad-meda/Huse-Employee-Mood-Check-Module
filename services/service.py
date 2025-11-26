import re
from sqlalchemy.orm import Session
from Files.SQLAlchemyModels import Employee



class EmployeeService:

    @staticmethod
    def get_employee_record(contact_number: str, db_session: Session):
        #gets all the record of the employee based on their contact number
        contact_number = None if contact_number is None else re.sub(r'[^\d]', '', str(contact_number))
        try:
            employee = db_session.query(Employee).filter(
                Employee.contactNo == contact_number
            ).first()
            if employee is None:
                raise ValueError(f"No employee found with contact number: {contact_number}")
            return employee
        except Exception as e:
            raise Exception(f"Error retrieving employee by contact number {contact_number}: {str(e)}")
        


  