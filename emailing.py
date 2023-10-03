import smtplib
from email.message import EmailMessage
import imghdr

password = "slutycgycmzuhfpq"
sender = "robert.horvath93@gmail.com"
receiver = "robert.horvath93@gmail.com"


def send_email(image_path):
    print("send_email function started")
    email_message = EmailMessage()
    email_message["Subject"] = "Object detected"
    email_message.set_content("An object has been detected !")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)  # 587 is the port for gmail
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()
    print("send_email function ended")


if __name__ == "__main__":
    send_email(image_path="images/3.png")
