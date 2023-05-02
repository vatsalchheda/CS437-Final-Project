import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from colorama import Fore, Style

# User imports
from config import emails

def send_mail(mode=1, usr_name="None", new_usr="None"):
    # Replace these with your own email and password
    your_email = "cs437.ravn@gmail.com"
    your_password = "ktstqhfmscaycekq" #safe

    if mode == 1:
        # Define the sender, recipient, subject, and message
        ems = list(emails.values())
        from_email = your_email
        word = "[URGENT]"
        formatted_word = word
        subject = formatted_word + "RAVN Security System -- Activity information."
        message = "RAVN Security System thinks that the vault's security was compromised. Details of the intrusion (log and image) are attached for your reference. consider calling 911 immidiately!"

        # Define the attachment file path
        attachment_file_path = 'Activity_log.txt'  # Replace with the path to your attachment

        # Create a MIMEMultipart object and set the required headers
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['Subject'] = subject

        # Attach the message to the MIMEMultipart object
        msg.attach(MIMEText(message, 'plain'))

        # Attach the file
        with open(attachment_file_path, 'rb') as attachment_file:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(attachment_file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_file_path)}')
            msg.attach(attachment)

        image_file_path = 'unlock_attempt.jpg'
        with open(image_file_path, 'rb') as file:
            img_data = file.read()
        image_attachment = MIMEImage(img_data)
        image_attachment.add_header('Content-Disposition', 'attachment', filename="image.jpg")
        msg.attach(image_attachment)

        # Establish a secure connection with the email server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            # Log in to your email account
            server.login(your_email, your_password)

            # Send the email
            for to_em in ems:
                server.sendmail(from_email, to_em, msg.as_string())
                print("Email sent successfully!")

        # Print a success message
        print("Execution completed!")
    elif mode == 2:
        # Define the sender, recipient, subject, and message
        ems = list(emails.values())
        from_email = your_email
        word = "[UPDATE]"
        formatted_word = word
        subject = formatted_word + "RAVN Security System -- Activity Update."
        message = "RAVN Security ::: " +  str(usr_name) + "added another user,  " + str(new_usr) + ". Details of the activity (log file) is attached for your reference"

        # Define the attachment file path
        attachment_file_path = 'Activity_log.txt'  # Replace with the path to your attachment

        # Create a MIMEMultipart object and set the required headers
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['Subject'] = subject

        # Attach the message to the MIMEMultipart object
        msg.attach(MIMEText(message, 'plain'))

        # Attach the file
        with open(attachment_file_path, 'rb') as attachment_file:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(attachment_file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_file_path)}')
            msg.attach(attachment)

        # Establish a secure connection with the email server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            # Log in to your email account
            server.login(your_email, your_password)

            # Send the email
            for to_em in ems:
                server.sendmail(from_email, to_em, msg.as_string())
                print("Email sent successfully!")

        # Print a success message
        print("Execution completed!")
