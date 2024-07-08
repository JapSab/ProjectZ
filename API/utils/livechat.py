import requests
from API import LIVECHAT_BASE_URL, LIVECHAT_API_VERSION, LIVECHAT_ORGANIZATION_ID, LIVECHAT_CLIENT_ID

ENDPOINTS = {
    "list_chats" : f"{LIVECHAT_BASE_URL}/{LIVECHAT_API_VERSION}/customer/action/list_chats?organization_id={LIVECHAT_ORGANIZATION_ID}",
    "start_chat": f'{LIVECHAT_BASE_URL}/{LIVECHAT_API_VERSION}/customer/action/start_chat?organization_id={LIVECHAT_ORGANIZATION_ID}',
    "get_chat": f'{LIVECHAT_BASE_URL}/{LIVECHAT_API_VERSION}/customer/action/get_chat?organization_id={LIVECHAT_ORGANIZATION_ID}',
    "resume_chat": f'{LIVECHAT_BASE_URL}/{LIVECHAT_API_VERSION}/customer/action/resume_chat?organization_id={LIVECHAT_ORGANIZATION_ID}',
    "deactive_chat": f'{LIVECHAT_BASE_URL}/{LIVECHAT_API_VERSION}/customer/action/deactivate_chat?organization_id={LIVECHAT_ORGANIZATION_ID}',
    "update_customer": f"{LIVECHAT_BASE_URL}/{LIVECHAT_API_VERSION}/customer/action/update_customer?organization_id={LIVECHAT_ORGANIZATION_ID}",
    "send_event": f"{LIVECHAT_BASE_URL}/{LIVECHAT_API_VERSION}/customer/action/send_event?organization_id={LIVECHAT_ORGANIZATION_ID}"
}

def call_livechat_api(action, params=None, headers=None):
    endpoint = ENDPOINTS.get(action)
    if not endpoint:
        raise Exception(f"Endpoint {action} not found")

    if action == "list_chats":
        payload = {}
    elif action == "get_chat":
        chat_id = params.get("chat_id")
        if not chat_id:
            raise ValueError(f"{chat_id} Missing chat_id for get_chat action")
        payload = {
            "chat_id": chat_id,
        }
    elif action == "start_chat":
        payload = {}
    elif action == "update_customer":
        name = params.get("name")
        email = params.get("email")
        if not name:
            raise ValueError("Missing parameters for update action")
        payload = {
            "name": name,
            "email": email
        }
    elif action == "send_event":
        email = params.get("email")
        has_payed = redis_cache.get(f"chat_expiration:{email}")
        if has_payed:
            chat_id = params.get("chat_id")
            event = params.get("event")
            if not chat_id or not event:
                raise ValueError("Missing parameters for send_event action")
            payload = {
                "chat_id": chat_id,
                "event": event
            }
        else:
            raise Exception(f"The user hasn't payed")
    else:
        raise Exception(f"Unsupported action: {action}")
    
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