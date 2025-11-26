import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_all_contacts_from_api():
    """Get all contact numbers from Huse API"""
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
            contacts = []
            
            for user in users:
                if isinstance(user, dict):
                    # Check both 'contact' and 'phone' fields
                    contact = user.get('contact') or user.get('phone')
                    if contact:
                        contact = contact.strip()
                        if contact:
                            contacts.append(contact)
            
            print(f"Retrieved {len(contacts)} contact numbers from API")
            return contacts
        else:
            print(f"API Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error getting contacts from API: {e}")
        return []
