import requests
from API import API_VERSION, ORGANIZATION_ID

ENDPOINTS = {
    "list_chats" : f"https://api.livechatinc.com/{API_VERSION}/customer/action/list_chats?organization_id={ORGANIZATION_ID}",
    "start_chat": f'https://api.livechatinc.com/{API_VERSION}/customer/action/start_chat?organization_id={ORGANIZATION_ID}',
    "get_chat": f'https://api.livechatinc.com/{API_VERSION}/customer/action/get_chat?organization_id={ORGANIZATION_ID}',
    "resume_chat": f'https://api.livechatinc.com/{API_VERSION}/customer/action/resume_chat?organization_id={ORGANIZATION_ID}',
    "deactive_chat": f'https://api.livechatinc.com/{API_VERSION}/customer/action/deactivate_chat?organization_id={ORGANIZATION_ID}',
    "update_customer": f"https://api.livechatinc.com/{API_VERSION}/customer/action/update_customer?organization_id={ORGANIZATION_ID}"
}


def call_livechat_api(action, params=None, headers=None):
    endpoint = ENDPOINTS.get(action)
    if not endpoint:
        raise Exception(f"Endpoint {action} not found")

    if action == "list_chats":
        payload = {}
    elif action == "get_chat":
        chat_id = params.get("chat_id")
        thread_id = params.get("thread_id")
        if not chat_id or not thread_id:
            raise ValueError("Missing chat_id or thread_id for get_chat action")
        payload = {
            "chat_id": chat_id,
            "thread_id": thread_id
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
    
    else:
        raise Exception(f"Unsupported action: {action}")

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error calling LiveChat API: {str(e)}")

    return response.json()