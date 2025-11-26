import redis
import json

class EmployeeSessionService:
    def __init__(self):
        # Connect to Redis Cloud server
        self.redis_client = redis.Redis(
            host='redis-10661.c17.us-east-1-4.ec2.redns.redis-cloud.com',
            port=10661,
            decode_responses=True,
            username="default",
            password="RKWH5tuWOhrxTsrAsJucYSCuUjdBXpPa"
        )
    
    def set_employee_identified(self, contact_number, is_identified):
        """Set employee identified status"""
        key = f"employee:identified:{contact_number}"
        value = "1" if is_identified else "0"
        # Store for 24 hours (86400 seconds)
        self.redis_client.set(key, value, ex=86400)
    
    def get_employee_identified(self, contact_number):
        """Get employee identified status"""
        key = f"employee:identified:{contact_number}"
        value = self.redis_client.get(key)
        return value == "1"
    
    def set_employee_id(self, contact_number, employee_id):
        """Set employee ID"""
        key = f"employee:id:{contact_number}"
        # Store for 24 hours (86400 seconds)
        self.redis_client.set(key, employee_id, ex=86400)
    
    def get_employee_id(self, contact_number):
        """Get employee ID"""
        key = f"employee:id:{contact_number}"
        return self.redis_client.get(key)
    
    def clear_employee_session(self, contact_number):
        """Clear all employee data for this contact"""
        identified_key = f"employee:identified:{contact_number}"
        id_key = f"employee:id:{contact_number}"
        
        self.redis_client.delete(identified_key)
        self.redis_client.delete(id_key)

    def add_to_list(self, contact_number, items):
        key = f"contact_list:{contact_number}"
        for item in items:
            self.redis_client.rpush(key, item)
    
    def clear_list(self, contact_number):
        key = f"contact_list:{contact_number}"
        self.redis_client.delete(key)
    
    def get_list(self, contact_number):
        key = f"contact_list:{contact_number}"
        return self.redis_client.lrange(key, 0, -1)
    
    def clear_messages(self, contact_number: str):
        """Clear all messages for a given contact number"""
        key = f"contact:{contact_number}:messages"
        self.redis_client.delete(key)
    
    def add_message(self, contact_number: str, message: dict):
        """Add a message to the contact's history"""
        key = f"contact:{contact_number}:messages"
        self.redis_client.rpush(key, json.dumps(message))
    
    def get_messages(self, contact_number: str) -> list:
        """Get all messages for a given contact number"""
        key = f"contact:{contact_number}:messages"
        messages = self.redis_client.lrange(key, 0, -1)
        return [json.loads(msg) for msg in messages]
    
    def set_multiple_office_locations(self, contact_number: str, location_names: list):
        """Set the multiple office locations list for a contact"""
        key = f"contact:{contact_number}:multiple_office_locations"
        # Store as JSON string for 24 hours (86400 seconds)
        self.redis_client.set(key, json.dumps(location_names), ex=86400)
    
    def get_multiple_office_locations(self, contact_number: str) -> list:
        """Get the multiple office locations list for a contact"""
        key = f"contact:{contact_number}:multiple_office_locations"
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return []
    
    def clear_multiple_office_locations(self, contact_number: str):
        """Clear the multiple office locations list for a contact"""
        key = f"contact:{contact_number}:multiple_office_locations"
        self.redis_client.delete(key)
    
    def set_asked_confirmation(self, contact_number: str, asked_confirmation: bool):
        """Set asked confirmation status for a contact"""
        key = f"contact:{contact_number}:asked_confirmation"
        value = "1" if asked_confirmation else "0"
        # Store for 24 hours (86400 seconds)
        self.redis_client.set(key, value, ex=86400)
    
    def get_asked_confirmation(self, contact_number: str) -> bool:
        """Get asked confirmation status for a contact"""
        key = f"contact:{contact_number}:asked_confirmation"
        value = self.redis_client.get(key)
        return value == "1" if value is not None else False
    
    def clear_asked_confirmation(self, contact_number: str):
        """Clear asked confirmation status for a contact"""
        key = f"contact:{contact_number}:asked_confirmation"
        self.redis_client.delete(key)

    def set_employee_asked_confirmation(self, contact_number: str, asked_confirmation: bool):
        """Set asked confirmation status for an employee"""
        key = f"employee:{contact_number}:asked_confirmation"
        value = "1" if asked_confirmation else "0"
        # Store for 24 hours (86400 seconds)
        self.redis_client.set(key, value, ex=86400)
    
    def get_employee_asked_confirmation(self, contact_number: str) -> bool:
        """Get asked confirmation status for an employee"""
        key = f"employee:{contact_number}:asked_confirmation"
        value = self.redis_client.get(key)
        return value == "1" if value is not None else False
    
    def clear_employee_asked_confirmation(self, contact_number: str):
        """Clear asked confirmation status for an employee"""
        key = f"employee:{contact_number}:asked_confirmation"
        self.redis_client.delete(key)
    
    def set_employee_asked_user_feedback(self, contact_number: str, asked_feedback: bool):
        """Set asked user feedback status for an employee"""
        key = f"employee:{contact_number}:asked_user_feedback"
        value = "1" if asked_feedback else "0"
        self.redis_client.set(key, value, ex=86400)
    
    def get_employee_asked_user_feedback(self, contact_number: str) -> bool:
        """Get asked user feedback status for an employee"""
        key = f"employee:{contact_number}:asked_user_feedback"
        value = self.redis_client.get(key)
        return value == "1" if value is not None else False
    
    def clear_employee_asked_user_feedback(self, contact_number: str):
        """Clear asked user feedback status for an employee"""
        key = f"employee:{contact_number}:asked_user_feedback"
        self.redis_client.delete(key)
        
    def set_update_agent_confirmation(self, contact_number: str, confirmation: bool):
        """Set update agent confirmation status for a contact"""
        key = f"contact:{contact_number}:update_agent_confirmation"
        value = "1" if confirmation else "0"
        # Store for 24 hours (86400 seconds)
        self.redis_client.set(key, value, ex=86400)
    
    def get_update_agent_confirmation(self, contact_number: str) -> bool:
        """Get update agent confirmation status for a contact"""
        key = f"contact:{contact_number}:update_agent_confirmation"
        value = self.redis_client.get(key)
        return value == "1" if value is not None else False
    
    def clear_update_agent_confirmation(self, contact_number: str):
        """Clear update agent confirmation status for a contact"""
        key = f"contact:{contact_number}:update_agent_confirmation"
        self.redis_client.delete(key)
    
    def set_user_trying_to_add_new_employee(self, contact_number: str, trying_to_add: bool):
        """Set user trying to add new employee status for a contact"""
        key = f"contact:{contact_number}:user_trying_to_add_new_employee"
        value = "1" if trying_to_add else "0"
        # Store for 24 hours (86400 seconds)
        self.redis_client.set(key, value, ex=86400)
    
    def get_user_trying_to_add_new_employee(self, contact_number: str) -> bool:
        """Get user trying to add new employee status for a contact"""
        key = f"contact:{contact_number}:user_trying_to_add_new_employee"
        value = self.redis_client.get(key)
        return value == "1" if value is not None else False
    
    def clear_user_trying_to_add_new_employee(self, contact_number: str):
        """Clear user trying to add new employee status for a contact"""
        key = f"contact:{contact_number}:user_trying_to_add_new_employee"
        self.redis_client.delete(key)
    
    def set_asked_user_draft_continuation(self, contact_number: str, asked_continuation: bool):
        """Set asked user draft continuation status for a contact"""
        key = f"contact:{contact_number}:asked_user_draft_continuation"
        value = "1" if asked_continuation else "0"
        # Store for 24 hours (86400 seconds)
        self.redis_client.set(key, value, ex=86400)
    
    def get_asked_user_draft_continuation(self, contact_number: str) -> bool:
        """Get asked user draft continuation status for a contact"""
        key = f"contact:{contact_number}:asked_user_draft_continuation"
        value = self.redis_client.get(key)
        return value == "1" if value is not None else False
    
    def clear_asked_user_draft_continuation(self, contact_number: str):
        """Clear asked user draft continuation status for a contact"""
        key = f"contact:{contact_number}:asked_user_draft_continuation"
        self.redis_client.delete(key)
    
    def set_correcting_final_confirmation_changes(self, contact_number: str, correcting_changes: bool):
        """Set correcting final confirmation changes status for a contact"""
        key = f"contact:{contact_number}:correcting_final_confirmation_changes"
        value = "1" if correcting_changes else "0"
        # Store for 24 hours (86400 seconds)
        self.redis_client.set(key, value, ex=86400)
    
    def get_correcting_final_confirmation_changes(self, contact_number: str) -> bool:
        """Get correcting final confirmation changes status for a contact"""
        key = f"contact:{contact_number}:correcting_final_confirmation_changes"
        value = self.redis_client.get(key)
        return value == "1" if value is not None else False
    
    def clear_correcting_final_confirmation_changes(self, contact_number: str):
        """Clear correcting final confirmation changes status for a contact"""
        key = f"contact:{contact_number}:correcting_final_confirmation_changes"
        self.redis_client.delete(key)
    
    def get_field_confirmation_list(self, contact_number: str) -> dict:
        """Get all field-value pairs that were asked for confirmation"""
        key = f"contact:{contact_number}:field_confirmation_list"
        field_values = self.redis_client.hgetall(key)
        return field_values
    
    def add_field_to_confirmation_list(self, contact_number: str, field_name: str, field_value: str):
        """Add a field-value pair to the confirmation list"""
        key = f"contact:{contact_number}:field_confirmation_list"
        self.redis_client.hset(key, field_name, field_value)
        # Set expiration for 24 hours (86400 seconds)
        self.redis_client.expire(key, 86400)
    
    def remove_field_from_confirmation_list(self, contact_number: str, field_name: str):
        """Remove a specific field from the confirmation list"""
        key = f"contact:{contact_number}:field_confirmation_list"
        self.redis_client.hdel(key, field_name)
    
    def clear_field_confirmation_list(self, contact_number: str):
        """Clear all field confirmation data for a contact"""
        key = f"contact:{contact_number}:field_confirmation_list"
        self.redis_client.delete(key)
    
    def set_name_extracted(self, contact_number: str, name_extracted: bool):
        """Set name extracted status for a contact"""
        key = f"contact:{contact_number}:name_extracted"
        value = "1" if name_extracted else "0"
        # Store for 24 hours (86400 seconds)
        self.redis_client.set(key, value, ex=86400)
    
    def get_name_extracted(self, contact_number: str) -> bool:
        """Get name extracted status for a contact"""
        key = f"contact:{contact_number}:name_extracted"
        value = self.redis_client.get(key)
        return value == "1" if value is not None else False
    
    def clear_name_extracted(self, contact_number: str):
        """Clear name extracted status for a contact"""
        key = f"contact:{contact_number}:name_extracted"
        self.redis_client.delete(key)
    
    def set_shift_time(self, contact_number: str, time_value):
        """Set shift time for a contact (can be any type - will be stored as string)"""
        key = f"contact:{contact_number}:shift_time"
        value = str(time_value)
        # Store for 24 hours (86400 seconds)
        self.redis_client.set(key, value, ex=86400)
    
    def get_shift_time(self, contact_number: str):
        """Get shift time for a contact (returns None if not found)"""
        key = f"contact:{contact_number}:shift_time"
        return self.redis_client.get(key)
    
    def clear_shift_time(self, contact_number: str):
        """Clear shift time for a contact"""
        key = f"contact:{contact_number}:shift_time"
        self.redis_client.delete(key)