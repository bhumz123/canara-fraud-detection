import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "frauddetectioncanara@gmail.com"
password = "rjhnmpmxkrgagcbo"
receiver_email = "tomartanu647@gmail.com"


def send_email(event_key, trans_amount, trans_datetime):
    message = MIMEMultipart("alternative")
    message["Subject"] = f"URGENT Fraud Alert: Transaction ID {event_key}"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
Dear Admin,

Automated system has flagged a potentially fraudulent transaction. 

Transaction Details:

Transaction ID: {event_key}
Date/Time: {trans_datetime}
Amount: {trans_amount}

Your prompt attention to this matter is crucial in ensuring the security of our customer's account.

Sincerely,
Fraud Detection System

    """

    html = f"""\
    <html>
      <body>
        <p>Dear Admin,</p>
        <p>Automated system has flagged a potentially fraudulent transaction on your account.</p>
       <p>Transaction Details:</p>

        <p>
            Transaction ID: {event_key}<br/>
            Date/Time: {trans_datetime}<br/>
            Amount: {trans_amount}<br/>
        </p>

        <p>Your prompt attention to this matter is crucial in ensuring the security of our customer's account.</p>

        <p>Sincerely,<br/>
        Fraud Detection System
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    server = None
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP("smtp.gmail.com", port)
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()