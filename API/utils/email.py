import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
sender_email = 'your_email@example.com'
receiver_email = 'recipient@example.com'
password = 'your_password'

# Construct the email message
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = 'Test Email'

body = "This is a test email sent from Python."
message.attach(MIMEText(body, 'plain'))

# Connect to the SMTP server
with smtplib.SMTP('smtp.example.com', 587) as server:
    server.starttls()
    server.login(sender_email, password)

    # Send the email
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)

print("Email sent successfully!")
