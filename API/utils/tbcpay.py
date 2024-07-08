import requests
from API import TBCPAY_BASE_URL, TBCPAY_API_KEY, TBCPAY_API_VERSION, TBCPAY_CLIENT_ID, TBCPAY_CLIENT_SECRET

payment_id = "payment_id"

ENDPOINTS = {
    "get_token": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/access-token",
    "create_payment": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/payments",
    "get_payment": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/payments/:payment_id",
    "cancel_payment": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/payments/:payment_id/cancel",
    "complete_payment": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/payments/{payment_id}/completion",
}

def call_tbcpay_api(action, params):
    endpoint = ENDPOINTS.get(action)
    if not endpoint:
        raise Exception(f"Endpoint {action} not found")

    headers = {
        'apikey': TBCPAY_API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {}

    try:
        if action != "get_token":
            token_response = call_tbcpay_api("get_token", params={})
            token = token_response.get('access_token')
            headers['Authorization'] = f"Bearer {token}"

        if action == "get_token":
            payload = {
                "client_Id": TBCPAY_CLIENT_ID,
                "client_secret": TBCPAY_CLIENT_SECRET,
            }
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            response = requests.post(endpoint, headers=headers, data=payload)
        elif action == "create_payment":
            amount = params.get("amount")
            return_url = params.get("returnurl")

            payload['amount'] = amount
            payload['returnurl'] = return_url
            response = requests.post(endpoint, headers=headers, json=payload)
        elif action == "complete_payment":
            amount = params.get("amount")
            payment_id = params.get("payment_id")

            payload['amount'] = int(amount)

            if "payment_id" in endpoint:
                endpoint = endpoint.replace('payment_id', payment_id)
                
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