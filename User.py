from flask.ext.login import UserMixin
from DB import MyDB


class User(UserMixin):
    def __init__(self,id,username,password,realName):
        self.id=id
        self.userName=username
        self.password=password
        self.realName=realName

    def get_realName(self):
        return self.realName

    def get_userId(self):
        return self.id

    def get_id(self):
        return self.userName
