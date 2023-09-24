import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

subject = 'Test Email kwargs'
body = 'This is the body of the email testing kwargs in function'
sender = 'book.heatherrae@gmail.com'
recipient = 'jessebrusa@gmail.com'
password = 'gwar syjc svqr cern'

# Function to send an email with an attachment
def send_email_with_attachment(subject, body, recipient, **kwargs):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'book.heatherrae@gmail.com'
    msg['To'] = recipient

    msg.attach(MIMEText(body, 'plain'))

    if kwargs.get('attachment'):
        attachment_filename = kwargs.get('attachment')

        with open(attachment_filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
    
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {attachment_filename}')
        msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, 'gwar syjc svqr cern')
        smtp_server.sendmail(sender, recipient, msg.as_string())
    print('Message with attachment sent!')

# Call the function with the attachment filename
attachment_filename = 'static/location_img/Southgate.jpeg'  # Replace with your attachment file name
send_email_with_attachment(subject, body, sender, recipient, password, attachment=attachment_filename)


