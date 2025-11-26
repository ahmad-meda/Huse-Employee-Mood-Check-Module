from services.employee_choices_service import EmployeeChoicesService

class EmployeeChoicesProxy:

    @staticmethod
    def get_role_choices():
        from app import app, db
        with app.app_context():
            return EmployeeChoicesService.get_role_choices(db.session)
    
    @staticmethod
    def get_company_choices():
        from app import app, db
        with app.app_context():
            return EmployeeChoicesService.get_company_choices(db.session)
    
    @staticmethod
    def get_group_choices():
        from app import app, db
        with app.app_context():
            return EmployeeChoicesService.get_group_choices(db.session)
    
    @staticmethod
    def get_department_choices():
        from app import app, db
        with app.app_context():
            return EmployeeChoicesService.get_department_choices(db.session)
    
    @staticmethod
    def get_office_location_choices():
        from app import app, db
        with app.app_context():
            return EmployeeChoicesService.get_office_location_choices(db.session)

    @staticmethod
    def get_work_policy_choices():
        from app import app, db
        with app.app_context():
            return EmployeeChoicesService.get_work_policy_choices(db.session)
    
    @staticmethod
    def get_gender_choices():
        from app import app, db
        with app.app_context():
            return EmployeeChoicesService.get_gender_choices(db.session)