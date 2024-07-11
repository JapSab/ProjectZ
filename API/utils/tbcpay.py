import requests
from API import TBCPAY_BASE_URL, TBCPAY_API_KEY, TBCPAY_API_VERSION, TBCPAY_CLIENT_ID, TBCPAY_CLIENT_SECRET, redis_cache

ENDPOINTS = {
    "get_token": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/access-token",
    "create_payment": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/payments",
    "get_payment": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/payments/",
    "cancel_payment": f"{TBCPAY_BASE_URL}/{TBCPAY_API_VERSION}/tpay/payments/:payment_id/cancel",
}

PACKAGE_PRICES = {
    1: {"currency": "GEL", "total": 0.1, "subTotal": 0, "tax": 0, "shipping": 0},
    2: {"currency": "GEL", "total": 50, "subTotal": 0, "tax": 0, "shipping": 0},
    3: {"currency": "GEL", "total": 80, "subTotal": 0, "tax": 0, "shipping": 0}
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
            package_id = params.get("packageId")
            return_url = params.get("returnurl")
            email = params.get("email")
            
            if package_id not in PACKAGE_PRICES:
                raise ValueError("Invalid package ID")

            amount = PACKAGE_PRICES[package_id]

            payload['amount'] = amount
            payload['returnurl'] = return_url

            response = requests.post(endpoint, headers=headers, json=payload)

        elif action == "get_payment":
            email = params.get("email")
            payment_id = params.get("payment_id")
            expiration_time = 1800
            if payment_id:
                url = f"{endpoint}/{payment_id}"
                params = {'payment_id': payment_id}

                response = requests.get(url, headers=headers)
                response_data = response.json()
                if response_data["status"] == "Succeeded":
                    etnry_exists = redis_cache.get(f"chat_expiration:{email}")
                    if etnry_exists == None:
                        if response_data["amount"] == 0.1:
                            expiration_time = 1800 # 30 minutes
                        elif response_data["amount"] == 50:
                            expiration_time = 5400  # 1 hour
                        elif response_data["amount"] == 80:
                            expiration_time = 7200  # 2 hours
                        redis_cache.set(f"chat_expiration:{email}", response_data["amount"], ex=expiration_time)

                        return {"Succeeded": True}
                else:
                    return {"Succeeded": False, "message": "You have not purchased a package, or your payed time has run out, please purchase a package to continue"}
            else:
                etnry_exists = redis_cache.get(f"chat_expiration:{email}")
                if etnry_exists:
                    return {"Succeeded": True}
                else:
                    print('here')
                    return {"Succeeded": False, "message": "You have not purchased a package, or your payed time has run out, please purchase a package to continue"}

       
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