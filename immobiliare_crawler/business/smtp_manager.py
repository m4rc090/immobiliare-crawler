import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List


class SmtpManager:
    def __init__(self, sender: str, receivers: List[str], password: str):
        self.sender = sender
        self.receivers = receivers
        self.password = password

    def send(self, dt: datetime, attachment_path: str = None):

        msg = MIMEMultipart()

        msg['From'] = self.sender
        msg['To'] = ",".join(self.receivers)
        msg['Subject'] = "Report automatico case {}".format(str(dt))

        body = "Ciao, ecco le case di oggi da Immobiliare"

        msg.attach(MIMEText(body, 'plain'))

        if attachment_path:
            path_obj = Path(attachment_path)
            filename = path_obj.name
            attachment = open(attachment_path, "rb")

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.sender, self.password)
        text = msg.as_string()
        server.sendmail(self.sender, self.receivers, text)
        server.quit()