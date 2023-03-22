import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:

    def __init__(self, login: str, pwd: str):
        self.login = login
        self.pwd = pwd
        self.smtp = "smtp.gmail.com"
        self.imap = "imap.gmail.com"
        self.smtp_port = 587

    def send_message(self, subject: str, recipients: list, message: str):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        ms = smtplib.SMTP(self.smtp, self.smtp_port)
        # identify ourselves to smtp gmail client
        ms.ehlo()
        # secure our email with tls encryption
        ms.starttls()
        # re-identify ourselves as an encrypted connection
        ms.ehlo()

        ms.login(self.login, self.pwd)
        ms.sendmail(self.login, ms, msg.as_string())
        ms.quit()

    def receive(self, header=None):
        imap = imaplib.IMAP4_SSL(self.imap)
        imap.login(self.login, self.pwd)
        imap.list()
        imap.select("inbox")
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = imap.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = imap.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        imap.logout()
        return email_message


if __name__ == '__main__':
    mail = Mail('login@gmail.com', 'qwerty')
    mail.send_message('Subject', ['vasya@email.com', 'petya@email.com'], 'Message')
    print(mail.receive())
