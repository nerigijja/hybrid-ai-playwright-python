# Update the import path below if your APIClient is located elsewhere
# For example, if api_client.py is in the same directory as this file:
# from .api_client import APIClient

# Placeholder import; update as needed:
from executables.api.api_client import APIClient

def get_json(api_client, endpoint):
    r = api_client.get(endpoint)
    return r.status_code, r.json()
