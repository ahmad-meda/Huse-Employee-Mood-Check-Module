from Files.SQLAlchemyModels import Role, Company, Department, Employee, OfficeLocation, Group, WorkPolicy
from sqlalchemy.orm import Session


class EmployeeChoicesService:

    @staticmethod
    def get_role_choices(db: Session):
        roles = db.query(Role).all()
        return [role.name for role in roles]

    @staticmethod
    def get_company_choices(db: Session):
        # Return all companies without any filter
        companies = db.query(Company).all()
        if not companies:
            return []
        return [company.name for company in companies]

    @staticmethod
    def get_department_choices(db: Session):
        departments = db.query(Department).all()
        return [department.name for department in departments]

    @staticmethod
    def get_office_location_choices(db: Session):
        office_locations = db.query(OfficeLocation).all()
        return [office_location.name for office_location in office_locations]
    
    @staticmethod
    def get_group_choices(db: Session):
        groups = db.query(Group).all()
        return [group.name for group in groups]
    
    @staticmethod
    def get_work_policy_choices(db:Session):
        work_policies = db.query(WorkPolicy).all()
        return [work_policy.name for work_policy in work_policies]
    
    @staticmethod
    def get_gender_choices(db:Session):
        #null fields are not included, get distinct values only
        genders = db.query(Employee.gender).filter(Employee.gender.isnot(None)).distinct().all()
        return [gender.gender for gender in genders]