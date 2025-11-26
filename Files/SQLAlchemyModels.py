from sqlalchemy import Double, Float, create_engine, Column, Integer, String, DateTime, Boolean, Text, Date, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timezone, date
import os
from dotenv import load_dotenv

from database import db

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:ias12345@localhost:5432/Employee")

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Association table for many-to-many relationship between Employee and OfficeLocation
allowed_office_locations = db.Table(
    'allowed_office_locations',
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True),
    db.Column('office_location_id', db.Integer, db.ForeignKey('office_locations.id'), primary_key=True)
)

draft_allowed_office_locations = db.Table(
    'draft_allowed_office_locations',
    db.Column('draft_employee_id', db.Integer, primary_key=True),
    db.Column('office_location_id', db.Integer, primary_key=True)
)

class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employeeId = db.Column(db.String(50), nullable=True)

    # 🔤 Name breakdown (new fields)
    first_name = db.Column(db.String(50), nullable=True)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)

    # 🧾 Keep full name for legacy code support
    name = db.Column(db.String, nullable=True)

    emailId = db.Column(db.String(100), nullable=True)
    designation = db.Column(db.String, nullable=True)
    dateOfJoining = db.Column(Date, nullable=True)

    dateOfBirth = db.Column(db.Date, nullable=True)
    contactNo = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=True)

    # 🔗 Office Location (instead of latitude/longitude directly)
    office_location_id = db.Column(db.Integer, ForeignKey('office_locations.id'), nullable=True)
    office_location = relationship('OfficeLocation', backref='employee')

    allowed_office_locations = relationship(
        'OfficeLocation',
        secondary=allowed_office_locations,
        backref='employees'
    )
    

    work_policy_id = db.Column(db.Integer, ForeignKey('work_policies.id'), nullable=True)
    work_policy = relationship('WorkPolicy', backref='employee')

    # Optional home location if policy requires it
    home_latitude = db.Column(db.Float, nullable=True)
    home_longitude = db.Column(db.Float, nullable=True)

    # 🔗 Company and Reporting Hierarchy
    company_id = db.Column(db.Integer, ForeignKey('companies.id'), nullable=True)
    company = relationship('Company', backref='employee')

    group_id = db.Column(db.Integer, ForeignKey('groups.id'), nullable=True)
    group = relationship('Group', backref='employee')

    reporting_manager_id = db.Column(db.Integer, ForeignKey('employee.id'), nullable=True)
    reporting_manager = relationship("Employee", remote_side=[id], backref="subordinates")

    # 🔗 Roles and Department
    role_id = db.Column(db.Integer, ForeignKey('role.id'), nullable=True)
    department_id = db.Column(db.Integer, ForeignKey('department.id'), nullable=True)

    role = relationship('Role', back_populates='employee')
    department = relationship('Department', back_populates='employee')
    reminders = db.Column(db.Boolean, nullable=False, default=True)
    allowed_company_ids = db.Column(db.JSON, nullable=True)
    is_hr = db.Column(db.Boolean, default=False, nullable=False)
    hr_scope = db.Column(db.String, default="company")
    allow_site_checkin = db.Column(db.Boolean, default=False)
    restrict_to_allowed_locations = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)
    username = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=True)

    # 🔗 Leave Requests and Balances
    leave_requests = relationship(
        "LeaveRequest",
        back_populates="employee",
        cascade="all, delete",
        foreign_keys="[LeaveRequest.employee_id]"
    )

    leave_balances = relationship(
        "LeaveBalance",
        back_populates="employee",
        cascade="all, delete",
        foreign_keys="[LeaveBalance.employee_id]"
    )
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    attendance = relationship("Attendance", back_populates="employee")
    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.name}')>"
    
class EmployeeDraft(db.Model):
    __tablename__ = "draft_employee"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(50), nullable=True)

    # 🔤 Name breakdown (new fields)
    first_name = db.Column(db.String(50), nullable=True)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)

    # 🧾 Keep full name for legacy code support
    name = db.Column(db.String, nullable=True)

    email_id = db.Column(db.String(100), nullable=True)
    designation = db.Column(db.String, nullable=True)
    date_of_joining = db.Column(Date, nullable=True)

    date_of_birth = db.Column(Date, nullable=True)
    contact_no = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=True)

    # 🔗 Office Location (instead of latitude/longitude directly)
    office_location_id = db.Column(db.Integer, nullable=True)

    # Note: allowed_office_locations relationship removed due to foreign key removal

    work_policy_id = db.Column(db.Integer, nullable=True)

    # Optional home location if policy requires it
    home_latitude = db.Column(db.Float, nullable=True)
    home_longitude = db.Column(db.Float, nullable=True)

    # 🔗 Company and Reporting Hierarchy
    company_id = db.Column(db.Integer, nullable=True)

    group_id = db.Column(db.Integer, nullable=True)

    reporting_manager_id = db.Column(db.Integer, nullable=True)

    # 🔗 Roles and Department
    role_id = db.Column(db.Integer, nullable=True)
    department_id = db.Column(db.Integer, nullable=True)

    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    reminders = db.Column(db.Boolean, nullable=False, default=True)
    allowed_company_ids = db.Column(db.JSON, nullable=True)
    is_hr = db.Column(db.Boolean, default=False, nullable=False)
    hr_scope = db.Column(db.String, default="company")
    allow_site_checkin = db.Column(db.Boolean, default=False)
    restrict_to_allowed_locations = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<EmployeeDraft(id={self.id}, name='{self.name}')>"

class Company(db.Model):
    __tablename__ = "companies"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prefix = db.Column(db.String(10))
    name = db.Column(db.String(255), nullable=False)
    group_id = db.Column(db.Integer, ForeignKey("groups.id"))
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"


class Group(db.Model):
    __tablename__ = "groups"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"


class Role(db.Model):
    __tablename__ = "role"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    # Add this relationship back to Employee
    employee = relationship('Employee', back_populates='role')
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"


class Department(db.Model):
    __tablename__ = "department"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    # Add this relationship back to Employee
    employee = relationship('Employee', back_populates='department')
    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}')>"


# class ReportingManager(Base):
#     __tablename__ = "reporting_managers"
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     manager_name = Column(String(255), nullable=False)
    
#     def __repr__(self):
#         return f"<ReportingManager(id={self.id}, manager_name='{self.manager_name}')>"


class OfficeLocation(db.Model):
    __tablename__ = "office_locations"
    
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # name = db.Column(db.String(255), nullable=False)
    id = db.Column(db.Integer, primary_key=True)    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)    
    name = db.Column(db.String(100), nullable=False)    
    address = db.Column(db.Text, nullable=True)    
    latitude = db.Column(db.Float, nullable=True)    
    longitude = db.Column(db.Float, nullable=True)    
    radius_meters = db.Column(db.Float, default=500)    
    is_active = db.Column(db.Boolean, default=True)    
    created_at = db.Column(db.DateTime, default=db.func.now())    
    company = db.relationship("Company", backref=db.backref("office_locations", lazy=True))    
    
    def __repr__(self):        return f"<OfficeLocation {self.name} - Company {self.company_id}>"
    
class WorkPolicy(db.Model):
    __tablename__ = "work_policies"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<WorkPolicy(id={self.id}, name='{self.name}')>"
    
class Draft(db.Model):
    __tablename__ = "drafts"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    draft_id = db.Column(db.String(100))
    draft_type = db.Column(db.String(100))
    employee_id = db.Column(db.Integer)
    
    def __repr__(self):
        return f"<Draft(id={self.id}, draft_id='{self.draft_id}', draft_type='{self.draft_type}')>"
    


class LeadMessageHistory(db.Model):
    __tablename__ = "messages"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_number = db.Column(db.String)
    role = db.Column(db.String)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<LeadMessageHistory(id={self.id}, contact_number='{self.contact_number}', role='{self.role}', timestamp='{self.timestamp}')>"
    
class Attendance(db.Model):
    __tablename__ = 'attendance'  

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, ForeignKey('employee.id'), nullable=False)
    employee = relationship('Employee', back_populates='attendance')

    check_in_time = db.Column(db.DateTime)
    check_out_time = db.Column(db.DateTime)

    working_hours = db.Column(db.Double)

    date = db.Column(db.Date)

    IsCheckInRequest = db.Column(db.Boolean)
    IsCheckOutRequest = db.Column(db.Boolean)

    is_active = db.Column(db.Boolean)

    employee = relationship('Employee', back_populates='attendance')

    def __repr__(self):
        return f"<Attendance(id={self.id}, employee_id={self.employee_id}, date={self.date})>"

class SessionState(db.Model):
    __tablename__ = 'session_state'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_number = db.Column(db.String, nullable=False)
    session_key = db.Column(db.String, nullable=False)  # e.g., 'employee_identified', 'employee_id'
    session_value = db.Column(db.String, nullable=True)  # Store as string, convert as needed
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<SessionState(contact_number='{self.contact_number}', key='{self.session_key}', value='{self.session_value}')>"
    

class LeavePolicy(db.Model):
    __tablename__ = 'leave_policies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    request_type = db.Column(db.String, nullable=False)
    max_days = db.Column(db.Integer, nullable=False)  # Max leave days per year
    min_service_days = db.Column(db.Integer, nullable=False)  # When leave becomes available
    notice_period = db.Column(db.String, nullable=True)  # Notice period requirements
    documentation_required = db.Column(db.Boolean, default=False)  # Proof required?
    clubbing_rules = db.Column(db.String, nullable=True)  # Allowed to be combined?

    def __repr__(self):
        return f"<LeavePolicy {self.request_type}>"

class LeaveBalance(db.Model):
    __tablename__ = 'leave_balances'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    request_type = db.Column(db.String, nullable=False)
    balance = db.Column(db.Float, nullable=False)  # Remaining leave balance (supports half-day: 0.5)
    
    # Track creation and updates
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # ✅ Correct relationship reference
    employee = db.relationship("Employee", back_populates="leave_balances")
    # policy = db.relationship("LeavePolicy", backref="leave_balances")

    def __repr__(self):
        return f"<LeaveBalance {self.request_type} - {self.balance} days>"

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    request_type = db.Column(db.String, db.ForeignKey('leave_policies.request_type'))
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    duration = db.Column(db.Float, nullable=True)  # Supports half-day (0.5) leave
    # request_type IN ('LEAVE','WFH','REMOTE','ONSITE','TRAVEL')
    status = db.Column(db.String, default="Pending")  # Pending, Approved, Rejected
    reason = db.Column(db.String, nullable=True)
    requires_approval = db.Column(db.Boolean, default=False)  # If policy requires approval
    is_half_day = db.Column(db.Boolean, default=False)  # Flag for half-day leave
    created_at = db.Column(DateTime, default=datetime.utcnow())
    # ✅ Correct relationships
    employee = db.relationship(
        "Employee",
        foreign_keys=[employee_id],
        back_populates="leave_requests"
    )
    policy = db.relationship("LeavePolicy", backref="leave_requests")

    def __repr__(self):
        return f"<LeaveRequest {self.request_type} ({self.status})>"
    
class HuseApp(db.Model):
    __tablename__ = "huse_app"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    huse_app_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<HuseApp(id={self.id}, huse_app_id={self.huse_app_id})>"


class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_legal_name = db.Column(db.String, nullable=True)
    preferred_nickname = db.Column(db.String, nullable=True)
    date_of_birth = db.Column(db.String, nullable=True)
    nationality = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=True)
    email_address = db.Column(db.String, nullable=True, unique=True)
    suggested_membership_tier = db.Column(db.String, nullable=True)
    residential_address = db.Column(db.String, nullable=True)
    passport_number = db.Column(db.String, nullable=True)
    id_number = db.Column(db.String, nullable=True)
    occupation = db.Column(db.String, nullable=True)
    job_title = db.Column(db.String, nullable=True)
    linkedin_or_website = db.Column(db.String, nullable=True)
    education_background = db.Column(db.String, nullable=True)
    notable_affiliations = db.Column(db.String, nullable=True)
    agent_id = db.Column(db.String, nullable=False)
    lead_status = db.Column(db.String(50), nullable=True)
    lead_comments = db.Column(db.Text, nullable=True)
    crm_backend_id = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=True)
    conversion_status = db.Column(db.String, nullable=True)
    approval_status = db.Column(db.String, nullable=True, default="Pending")
    company = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Lead(id={self.id}, full_legal_name='{self.full_legal_name}', email_address='{self.email_address}')>"

class MoodCheck(db.Model):
    __tablename__ = "mood_checks"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    mood = db.Column(db.Enum('1', '2', '3', '4', name='mood_status'), nullable=False)  # 1=Great, 2=Good, 3=Okay, 4=Not so good
    comments = db.Column(db.Text, nullable=True)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.Date, nullable=False, default=date.today)
    
    def __repr__(self):
        return f"<MoodCheck(id={self.id}, employee_id={self.employee_id}, mood='{self.mood}')>"

class ShiftTemplate(db.Model):
    """
    Company-scoped reusable shift templates with policy rules.
    Supports any start/end times, including cross-midnight.
    """
    __tablename__ = "shift_templates"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    name = db.Column(db.String, nullable=False)                    # e.g., "Night", "Day"
    start_time = db.Column(db.Time, nullable=False)                # Local company time
    end_time = db.Column(db.Time, nullable=False)                  # Local company time
    crosses_midnight = db.Column(db.Boolean, nullable=False, default=False)

    # Policy knobs
    grace_in_minutes    = db.Column(db.SmallInteger, nullable=False, default=0)
    early_out_grace_min = db.Column(db.SmallInteger, nullable=False, default=0)
    break_minutes       = db.Column(db.SmallInteger, nullable=False, default=0)
    paid_break          = db.Column(db.Boolean, nullable=False, default=True)
    policy              = db.Column(db.JSON, nullable=True)        # Optional extra rules

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # Relationships
    company = db.relationship('Company', backref='shift_templates')

    __table_args__ = (
        db.UniqueConstraint("company_id", "name", name="uq_shift_templates_company_name"),
        db.CheckConstraint(
            "grace_in_minutes >= 0 AND early_out_grace_min >= 0 AND break_minutes >= 0",
            name="ck_shift_templates_nonneg"
        ),
        db.Index("ix_shift_templates_company", "company_id"),
    )

    def __repr__(self):
        return f"<ShiftTemplate id={self.id} name='{self.name}' company_id={self.company_id}>"

class ScheduleAssignment(db.Model):
    """
    Core schedule record.
    One row = this employee works [template or custom time] from start_date..end_date.
    Also used for one-day overrides (start_date == end_date, is_override=True).
    Supports split shifts via `segment`.
    """
    __tablename__ = "schedule_assignments"

    id = db.Column(db.Integer, primary_key=True)
    company_id  = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date   = db.Column(db.Date, nullable=False)  # inclusive; for 1-day override start=end

    # Prefer template; fall back to custom times when needed
    shift_template_id = db.Column(db.Integer, db.ForeignKey('shift_templates.id'), nullable=True)

    custom_start_time = db.Column(db.Time, nullable=True)
    custom_end_time   = db.Column(db.Time, nullable=True)
    custom_crosses_midnight = db.Column(db.Boolean, nullable=True)

    is_off      = db.Column(db.Boolean, nullable=False, default=False)   # explicit off-day
    is_override = db.Column(db.Boolean, nullable=False, default=False)   # higher priority for that day(s)
    segment     = db.Column(db.SmallInteger, nullable=False, default=1)  # split shift index (1..N)

    # Hospitality-friendly extras
    office_location_id = db.Column(db.Integer, db.ForeignKey('office_locations.id'), nullable=True)
    role_id            = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)  # ✅ fixed table name

    reason     = db.Column(db.Text)
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # Relationships
    employee = db.relationship('Employee', backref='schedule_assignments')
    shift_template = db.relationship('ShiftTemplate', backref='schedule_assignments')

    __table_args__ = (
        # For lookups and to avoid accidental duplicates in UI
        db.Index('ix_sched_emp_span_segment', 'company_id', 'employee_id', 'start_date', 'end_date', 'segment'),
        db.CheckConstraint(
            "("
            "(shift_template_id IS NOT NULL AND custom_start_time IS NULL AND custom_end_time IS NULL)"
            " OR "
            "(shift_template_id IS NULL AND custom_start_time IS NOT NULL AND custom_end_time IS NOT NULL)"
            " OR "
            "(is_off = TRUE)"  # if off, times/templates are ignored
            ")",
            name='ck_sched_template_or_custom_or_off'
        ),
        db.CheckConstraint('segment >= 1', name='ck_sched_segment_pos'),
    )

    def __repr__(self):
        return f"<ScheduleAssignment emp={self.employee_id} {self.start_date}..{self.end_date} seg={self.segment}>"
