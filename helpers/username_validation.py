import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_all_usernames_from_api():
    """Get all usernames from Huse API"""
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
            usernames = []
            
            for user in users:
                if isinstance(user, dict) and user.get('username'):
                    username = user.get('username').strip()
                    if username:
                        usernames.append(username)
            
            print(f"Retrieved {len(usernames)} usernames from API")
            return usernames
        else:
            print(f"API Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error getting usernames from API: {e}")
        return []