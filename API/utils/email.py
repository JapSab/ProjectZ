from API import MAILGUN_DOMAIN , MAILGUN_API_KEY , MAILGUN_SENDER_EMAIL
import requests

def send_verification_email(to_email, verification_link):

    domain = current_app.config['MAILGUN_DOMAIN']
    api_key = current_app.config['MAILGUN_API_KEY']
    sender_email = current_app.config['MAILGUN_SENDER_EMAIL']

    subject = "Email Verification"
    body_text = f"Please verify your email by clicking on the following link: {verification_link}"

    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": sender_email,
            "to": [to_email],
            "subject": subject,
            "text": body_text,
        }
    )
    
    return response.status_code == 200