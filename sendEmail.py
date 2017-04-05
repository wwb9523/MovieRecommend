import smtplib
from email.mime.text import MIMEText

class Email(object):
    def __init__(self,user='48450976@qq.com',pwd='vzsyalcnqusncahb',to=''):
        self._user = user
        self._pwd  = pwd
        self._to   = to

    def setMsg(self,message):
        self.msg = MIMEText(message)
        self.msg["Subject"] = "don't panic"
        self.msg["From"]    = self._user
        self.msg["To"]      = self._to

    def send(self,to,msg):
        self._to=to
        self.setMsg(msg)
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(self._user, self._pwd)
            s.sendmail(self._user,self._to, self.msg.as_string())
            s.quit()
            print("Success!")
        except smtplib.SMTPException:
            print("Falied")