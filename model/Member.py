from orm import Model


class Member(Model):
    username = str
    user_id = int
    access_hash = int
    media = str  # Telegram, Instagram, Basalam, etc
    channel = str  # Channel_name, Group_name, Page_name
    channel_id = int  # Channel_id

    def __init__(self, username, user_id, access_hash, media, channel, channel_id):
        self.username = username
        self.user_id = user_id
        self.access_hash = access_hash
        self.media = media
        self.channel = channel
        self.channel_id = channel_id
