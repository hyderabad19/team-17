from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import Config1

def sendM(subject,html_content,to):
    c1 = Config1()
    message = Mail(
        from_email='loopedu123@gmail.com',
        to_emails=to,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(c1.sapi())
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)