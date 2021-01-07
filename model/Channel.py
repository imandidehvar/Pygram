from orm import Model


class Channel(Model):
    channel_id = int
    channel_title = str

    def __init__(self, channel_id, channel_title):
        self.channel_id = channel_id
        self.channel_title = channel_title
