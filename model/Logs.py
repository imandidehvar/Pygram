from orm import Model
import datetime


class Log(Model):
    user_id = int
    date = datetime

    def __init__(self, user_id, date):
        self.user_id = user_id
        self.date = date
