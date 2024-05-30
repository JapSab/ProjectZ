import requests
from API import TBCPAY_BASE_URL, TBCPAY_API_KEY, TBCPAY_API_VERSION, TBCPAY_CLIENT_ID, TBCPAY_CLIENT_SECRET

ENDPOINTS = {
    "get_token": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/access-token",
    "create_payment": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/payments",
    "get_payment": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/payments:payment_id",
    "cancel_payment": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/payments/:payment_id/cancel",
    "complete_payment": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/payments/:payment_id/completion",
}

def call_tbcpay_api(action, params, headers=None):
    endpoint = ENDPOINTS.get(action)
    if not endpoint:
        raise Exception(f"Endpoint {action} not found")

    headers = {
        'apikey': TBCPAY_API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        "client_Id": TBCPAY_CLIENT_ID,
        "client_secret": TBCPAY_CLIENT_SECRET,
    }
        
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response is not None:
            print(f"Response Content: {response.content}")
        raise
    except Exception as err:
        print(f"An error occurred: {err}")
        raise