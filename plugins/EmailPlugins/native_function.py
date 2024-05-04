import os
import smtplib
from typing import Annotated
from email.message import EmailMessage
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from dotenv import load_dotenv

class Email:
    """
    Description: EmailHelpersPlugin provides a set of functions to help send mails.

    Usage:
        kernel.add_plugin(EmailHelpersPlugin(), plugin_name="email")

    Examples:
        {{email.send_email}} => Sends an email to the recipient with the email body(provided in the KernelArguments)
    """
    @kernel_function(name="sendEmail", description="Send Email to the recipient with the email body")
    def send_email(self, recipient: Annotated[str, "The recipient is an emailid string"], email_body: Annotated[str, "The email_body is a string"]):
        """
        Sends email to recipient with the provided email body    
        """
        load_dotenv()
        msg = EmailMessage()
        msg['Subject'] = 'Email Check'
        msg['From'] = os.getenv("fromEmail")
        email_password = os.getenv("emailPassword")

        # msg['From'] = "sapientatrising@gmail.com"
        # email_password = "avkn uaec macn zmua"
        msg['To'] = recipient


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(msg['From'], email_password)
            msg.set_content(email_body, subtype='plain')
            smtp.send_message(msg)
        print("Email Sent")
        # components.html(html_content, height =1000)
