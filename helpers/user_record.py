import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def get_huse_user_by_username(username):
    """Get complete Huse user record by username"""
    try:
        print(f"\n🔍 STEP 1: Getting user record for username: {username}")
        
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        if not base_url or not token:
            print("❌ Error: API_BASE_URL and API_AUTH_TOKEN must be set")
            return None
        
        headers = {"Authorization": token}
        
        # Use the search functionality to find user by username
        url = f"{base_url}/api/Users"
        params = {
            'PageSize': 1000000,
            'SearchString': username,
            'SearchBy': 'Username'
        }
        
        print(f"📡 STEP 2: Searching for user with API call:")
        print(f"   URL: {url}")
        print(f"   Params: {params}")
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        print(f"   Response Status: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"   Found {len(users)} user(s) in search results")
            
            # Get the user ID from the search results
            user_id = None
            if users and len(users) > 0:
                user_id = users[0].get('id')
                print(f"✅ STEP 3: Found user ID: {user_id} for username: {username}")
            else:
                print(f"❌ No user found with username: {username}")
                return None
            
            # Now get the complete user record using the full endpoint
            full_url = f"{base_url}/api/Users/full/{user_id}"
            print(f"📡 STEP 4: Getting complete user record:")
            print(f"   Full URL: {full_url}")
            
            full_response = requests.get(full_url, headers=headers, timeout=30)
            print(f"   Response Status: {full_response.status_code}")
            
            if full_response.status_code == 200:
                print(f"✅ STEP 5: Successfully retrieved complete user record for username: {username} (ID: {user_id})")
                user_data = full_response.json()
                print(f"   Record contains {len(user_data)} fields")
                print(f"   Key fields: ID={user_data.get('id')}, Name={user_data.get('name')}, Email={user_data.get('email')}, Contact={user_data.get('contact')}")
                return user_data
            else:
                print(f"❌ API Error getting full user record: {full_response.status_code}")
                print(f"   Error response: {full_response.text}")
                return None
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Error response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting user record from API: {e}")
        return None
        
def update_user_record(username, contact_number: Optional[str] = None, email: Optional[str] = None):
    """Get user record by username, then only update the contact or email"""
    try:
        print(f"\n🚀 STARTING UPDATE PROCESS for username: {username}")
        print(f"   Contact number to update: {contact_number}")
        print(f"   Email to update: {email}")
        
        # First get the current user record
        print(f"\n📋 STEP 1: Getting current user record...")
        user_record = get_huse_user_by_username(username)
        if not user_record:
            print(f"❌ User not found: {username}")
            return None
        
        print(f"✅ Successfully retrieved user record")
        
        # ONLY update the specific fields requested - DO NOT touch any other fields
        # The user record from get_huse_user_by_username already contains all the data
        # We only modify the fields that were explicitly requested
        
        print(f"\n🔄 STEP 2: Preparing record for update...")
        # Create a copy to avoid modifying the original record
        updated_record = user_record.copy()
        print(f"   Created copy of record with {len(updated_record)} fields")
        
        # Only update contact if provided
        if contact_number is not None:
            old_contact = updated_record.get('contact')
            updated_record['contact'] = contact_number
            print(f"Updating contact number to: {contact_number}")
        
        # Only update email if provided  
        if email is not None:
            old_email = updated_record.get('email')
            updated_record['email'] = email
            print(f"📧 UPDATING EMAIL: '{old_email}' → '{email}'")
        else:
            print(f"📧 Email: No change requested")
        
        # IMPORTANT: All other fields remain EXACTLY the same as they were
        # The API requires the complete record with all original values preserved
        
        print(f"\n🔍 STEP 3: Verifying record before sending to API...")
        print(f"   Total fields in record: {len(updated_record)}")
        print(f"   Contact field: {updated_record.get('contact')}")
        print(f"   Email field: {updated_record.get('email')}")
        print(f"   SecurityAnswer field: {updated_record.get('securityAnswer')}")
        print(f"   PasswordHash field: {updated_record.get('passwordHash', 'N/A')[:20]}...")
        
        # Make the API call to update the user using /api/Users endpoint
        print(f"\n📡 STEP 4: Sending update request to API...")
        base_url = os.environ.get('API_BASE_URL')
        token = os.environ.get('API_AUTH_TOKEN')
        
        if not base_url or not token:
            print("❌ Error: API_BASE_URL and API_AUTH_TOKEN must be set")
            return None
        
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        url = f"{base_url}/api/Users"
        
        print(f"   API URL: {url}")
        print(f"   Request method: PUT")
        print(f"   Headers: {headers}")
        print(f"   Request payload (first 500 chars): {str(updated_record)[:500]}...")
        
        response = requests.put(url, headers=headers, json=updated_record, timeout=30)
        
        print(f"   Response Status: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"✅ STEP 5: Successfully updated user record for: {username}")
            result = response.json()
            print(f"   Update result: {result}")
            
            # Verify the update by getting the record again
            print(f"\n🔍 STEP 6: Verifying the update by fetching the record again...")
            verify_record = get_huse_user_by_username(username)
            if verify_record:
                print(f"   Current email after update: {verify_record.get('email')}")
                print(f"   Current contact after update: {verify_record.get('contact')}")
            else:
                print(f"   Could not verify update - failed to fetch record")
            
            return result
        else:
            print(f"❌ API Error updating user: {response.status_code}")
            print(f"   Error response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error updating user record: {e}")
        return None

