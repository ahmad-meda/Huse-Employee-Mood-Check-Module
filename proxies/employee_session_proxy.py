from services.employee_session_service import EmployeeSessionService

class EmployeeSessionProxy:
    # Create one instance to use everywhere
    _service = EmployeeSessionService()
    
    @classmethod
    def set_employee_identified(cls, contact_number, is_identified):
        """Store if employee is identified"""
        return cls._service.set_employee_identified(contact_number, is_identified)
    
    @classmethod
    def get_employee_identified(cls, contact_number):
        """Get if employee is identified (returns False if not found)"""
        return cls._service.get_employee_identified(contact_number)
    
    @classmethod
    def set_employee_id(cls, contact_number, employee_id):
        """Store employee ID"""
        return cls._service.set_employee_id(contact_number, employee_id)
    
    @classmethod
    def get_employee_id(cls, contact_number):
        """Get employee ID (returns None if not found)"""
        return cls._service.get_employee_id(contact_number)
    
    @classmethod
    def clear_employee_session(cls, contact_number):
        """Clear all employee data for this contact"""
        return cls._service.clear_employee_session(contact_number)

    @classmethod
    def add_to_list(cls, contact_number, items):
        """Add items to list"""
        return cls._service.add_to_list(contact_number, items)
    
    @classmethod
    def clear_list(cls, contact_number):
        """Clear the list"""
        return cls._service.clear_list(contact_number)

    @classmethod
    def get_list(cls, contact_number):
        """Get the list"""
        return cls._service.get_list(contact_number)
    
    @classmethod
    def clear_messages(cls, contact_number):
        """Clear all messages for a given contact number"""
        return cls._service.clear_messages(contact_number)
    
    @classmethod
    def add_message(cls, contact_number, message):
        """Add a message to the contact's history"""
        return cls._service.add_message(contact_number, message)    

    @classmethod
    def get_messages(cls, contact_number):
        """Get all messages for a given contact number"""
        return cls._service.get_messages(contact_number)
    
    @classmethod
    def set_multiple_office_locations(cls, contact_number, location_names):
        """Set the multiple office locations list for a contact"""
        return cls._service.set_multiple_office_locations(contact_number, location_names)
    
    @classmethod
    def get_multiple_office_locations(cls, contact_number):
        """Get the multiple office locations list for a contact"""
        return cls._service.get_multiple_office_locations(contact_number)
    
    @classmethod
    def clear_multiple_office_locations(cls, contact_number):
        """Clear the multiple office locations list for a contact"""
        return cls._service.clear_multiple_office_locations(contact_number)
    
    @classmethod
    def set_asked_confirmation(cls, contact_number, asked_confirmation):
        """Set asked confirmation status for a contact"""
        return cls._service.set_asked_confirmation(contact_number, asked_confirmation)
    
    @classmethod
    def get_asked_confirmation(cls, contact_number):
        """Get asked confirmation status for a contact"""
        return cls._service.get_asked_confirmation(contact_number)
    
    @classmethod
    def clear_asked_confirmation(cls, contact_number):
        """Clear asked confirmation status for a contact"""
        return cls._service.clear_asked_confirmation(contact_number)


    @classmethod
    def set_employee_asked_confirmation(cls, contact_number, asked_confirmation):
        """Set asked confirmation status for an employee"""
        return cls._service.set_employee_asked_confirmation(contact_number, asked_confirmation)
    
    @classmethod
    def get_employee_asked_confirmation(cls, contact_number):
        """Get asked confirmation status for an employee"""
        return cls._service.get_employee_asked_confirmation(contact_number)

    @classmethod
    def clear_employee_asked_confirmation(cls, contact_number):
        """Clear asked confirmation status for an employee"""
        return cls._service.clear_employee_asked_confirmation(contact_number)

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

    @classmethod
    def set_update_agent_confirmation(cls, contact_number, confirmation):
        """Set update agent confirmation status for a contact"""
        return cls._service.set_update_agent_confirmation(contact_number, confirmation)
    
    @classmethod
    def get_update_agent_confirmation(cls, contact_number):
        """Get update agent confirmation status for a contact"""
        return cls._service.get_update_agent_confirmation(contact_number)
    
    @classmethod
    def clear_update_agent_confirmation(cls, contact_number):
        """Clear update agent confirmation status for a contact"""
        return cls._service.clear_update_agent_confirmation(contact_number)

    @classmethod
    def set_user_trying_to_add_new_employee(cls, contact_number, trying_to_add):
        """Set user trying to add new employee status for a contact"""
        return cls._service.set_user_trying_to_add_new_employee(contact_number, trying_to_add)
    
    @classmethod
    def get_user_trying_to_add_new_employee(cls, contact_number):
        """Get user trying to add new employee status for a contact"""
        return cls._service.get_user_trying_to_add_new_employee(contact_number)
    
    @classmethod
    def clear_user_trying_to_add_new_employee(cls, contact_number):
        """Clear user trying to add new employee status for a contact"""
        return cls._service.clear_user_trying_to_add_new_employee(contact_number)

    @classmethod
    def set_asked_user_draft_continuation(cls, contact_number, asked_continuation):
        """Set asked user draft continuation status for a contact"""
        return cls._service.set_asked_user_draft_continuation(contact_number, asked_continuation)
    
    @classmethod
    def get_asked_user_draft_continuation(cls, contact_number):
        """Get asked user draft continuation status for a contact"""
        return cls._service.get_asked_user_draft_continuation(contact_number)
    
    @classmethod
    def clear_asked_user_draft_continuation(cls, contact_number):
        """Clear asked user draft continuation status for a contact"""
        return cls._service.clear_asked_user_draft_continuation(contact_number)

    @classmethod
    def set_correcting_final_confirmation_changes(cls, contact_number, correcting_changes):
        """Set correcting final confirmation changes status for a contact"""
        return cls._service.set_correcting_final_confirmation_changes(contact_number, correcting_changes)
    
    @classmethod
    def get_correcting_final_confirmation_changes(cls, contact_number):
        """Get correcting final confirmation changes status for a contact"""
        return cls._service.get_correcting_final_confirmation_changes(contact_number)
    
    @classmethod
    def clear_correcting_final_confirmation_changes(cls, contact_number):
        """Clear correcting final confirmation changes status for a contact"""
        return cls._service.clear_correcting_final_confirmation_changes(contact_number)

    # Field Confirmation Functions
    @classmethod
    def get_field_confirmation_list(cls, contact_number):
        """Get all field-value pairs that were asked for confirmation"""
        return cls._service.get_field_confirmation_list(contact_number)
    
    @classmethod
    def add_field_to_confirmation_list(cls, contact_number, field_name, field_value):
        """Add a field-value pair to the confirmation list"""
        return cls._service.add_field_to_confirmation_list(contact_number, field_name, field_value)
    
    @classmethod
    def remove_field_from_confirmation_list(cls, contact_number, field_name):
        """Remove a specific field from the confirmation list"""
        return cls._service.remove_field_from_confirmation_list(contact_number, field_name)
    
    @classmethod
    def clear_field_confirmation_list(cls, contact_number):
        """Clear all field confirmation data for a contact"""
        return cls._service.clear_field_confirmation_list(contact_number)

    @classmethod
    def set_name_extracted(cls, contact_number, name_extracted):
        """Set name extracted status for a contact"""
        return cls._service.set_name_extracted(contact_number, name_extracted)
    
    @classmethod
    def get_name_extracted(cls, contact_number):
        """Get name extracted status for a contact (returns False if not found)"""
        return cls._service.get_name_extracted(contact_number)
    
    @classmethod
    def clear_name_extracted(cls, contact_number):
        """Clear name extracted status for a contact"""
        return cls._service.clear_name_extracted(contact_number)

    @classmethod
    def set_shift_time(cls, contact_number, time_value):
        """Set shift time for a contact (can be any type - will be stored as string)"""
        return cls._service.set_shift_time(contact_number, time_value)
    
    @classmethod
    def get_shift_time(cls, contact_number):
        """Get shift time for a contact (returns None if not found)"""
        return cls._service.get_shift_time(contact_number)
    
    @classmethod
    def clear_shift_time(cls, contact_number):
        """Clear shift time for a contact"""
        return cls._service.clear_shift_time(contact_number)

    