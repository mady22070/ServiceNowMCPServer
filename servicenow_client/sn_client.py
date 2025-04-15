import time
import requests
from config import (
    SN_INSTANCE_URL, SN_AUTH_METHOD,
    SN_USERNAME, SN_PASSWORD,
    SN_OAUTH_URL, SN_CLIENT_ID, SN_CLIENT_SECRET
)

# Global variables for OAuth token caching
_token = None
_token_expiry = 0

def get_oauth_token() -> str:
    global _token, _token_expiry
    if _token and _token_expiry > time.time():
        return _token
    data = {
        "grant_type": "client_credentials",
        "client_id": SN_CLIENT_ID,
        "client_secret": SN_CLIENT_SECRET,
    }
    response = requests.post(SN_OAUTH_URL, data=data)
    response.raise_for_status()
    token_data = response.json()
    _token = token_data["access_token"]
    _token_expiry = time.time() + token_data["expires_in"] - 60  # buffer 60 seconds
    return _token

def create_record(table: str, data: dict) -> dict:
    url = f"{SN_INSTANCE_URL}/api/now/table/{table}"
    if SN_AUTH_METHOD == "oauth":
        headers = {"Authorization": f"Bearer {get_oauth_token()}"}
        response = requests.post(url, headers=headers, json=data)
    else:
        response = requests.post(url, auth=(SN_USERNAME, SN_PASSWORD), json=data)
    response.raise_for_status()
    return response.json()

def read_record(table: str, sys_id: str) -> dict:
    url = f"{SN_INSTANCE_URL}/api/now/table/{table}/{sys_id}"
    if SN_AUTH_METHOD == "oauth":
        headers = {"Authorization": f"Bearer {get_oauth_token()}"}
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url, auth=(SN_USERNAME, SN_PASSWORD))
    response.raise_for_status()
    return response.json()

def update_record(table: str, sys_id: str, data: dict) -> dict:
    url = f"{SN_INSTANCE_URL}/api/now/table/{table}/{sys_id}"
    if SN_AUTH_METHOD == "oauth":
        headers = {"Authorization": f"Bearer {get_oauth_token()}"}
        response = requests.put(url, headers=headers, json=data)
    else:
        response = requests.put(url, auth=(SN_USERNAME, SN_PASSWORD), json=data)
    response.raise_for_status()
    return response.json()

def delete_record(table: str, sys_id: str) -> dict:
    url = f"{SN_INSTANCE_URL}/api/now/table/{table}/{sys_id}"
    if SN_AUTH_METHOD == "oauth":
        headers = {"Authorization": f"Bearer {get_oauth_token()}"}
        response = requests.delete(url, headers=headers)
    else:
        response = requests.delete(url, auth=(SN_USERNAME, SN_PASSWORD))
    response.raise_for_status()
    return response.json()

def query_records(table: str, query: str, limit: int = 100, offset: int = 0) -> dict:
    url = f"{SN_INSTANCE_URL}/api/now/table/{table}?sysparm_query={query}&sysparm_limit={limit}&sysparm_offset={offset}"
    if SN_AUTH_METHOD == "oauth":
        headers = {"Authorization": f"Bearer {get_oauth_token()}"}
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url, auth=(SN_USERNAME, SN_PASSWORD))
    response.raise_for_status()
    return response.json()
