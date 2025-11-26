import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_all_emails_from_api():
    """Get all email addresses from Huse API"""
    try:
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        if not base_url or not token:
            print("Error: API_BASE_URL and API_AUTH_TOKEN must be set")
            return []
        
        headers = {"Authorization": token}
        url = f"{base_url}/api/Users"
        params = {'PageSize': 10000000}
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            users = response.json()
            emails = []
            
            for user in users:
                if isinstance(user, dict) and user.get('email'):
                    email = user.get('email').strip()
                    if email:
                        emails.append(email)
            
            print(f"Retrieved {len(emails)} emails from API")
            return emails
        else:
            print(f"API Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error getting emails from API: {e}")
        return []
