import redis
import json

class EmployeeMoodSessionService:
    def __init__(self):
        # Connect to Redis Cloud server
        self.redis_client = redis.Redis(
            host='redis-10661.c17.us-east-1-4.ec2.redns.redis-cloud.com',
            port=10661,
            decode_responses=True,
            username="default",
            password="RKWH5tuWOhrxTsrAsJucYSCuUjdBXpPa"
        )
    
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