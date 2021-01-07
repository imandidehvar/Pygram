from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerUser
from telethon.tl.types import ChatForbidden
from telethon.tl.types import Message
from orm import Database
from tqdm import tqdm
from datetime import *
from model import Member, Channel, Logs
import time, random


def get_chats():
    chats = []
    last_date = None
    chunk_size = 200

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)
    return chats


def get_members(group):
    return client.get_participants(group, aggressive=False)


def send_message(members, message, cpo):
    try:
        counter = 0
        for user in tqdm(members):
            try:
                if user[1] is not None and user[1] != "None":
                    receiver = client.get_input_entity(user[1])
                else:
                    receiver = InputPeerUser(user[2], user[3])
            except:
                obj = Member.Model.manager().get(username=user[0])
                obj.deleted_at = 'deleted_account'
                obj.update()
                db.commit()

            if receiver is not None:
                client.send_message(receiver, get_message(member))
                Logs.Log(receiver.user_id, datetime.now()).save()
                db.commit()
                counter = counter + 1
                time.sleep(7)

            if counter >= cpo:
                time.sleep(60)
                counter = 0
    except ValueError:
        print(ValueError)


def forward_message(members, message_id, chat_id, cpo):
    try:
        counter = 0
        for user in tqdm(members):
            try:
                if user[1] is not None and user[1] != "None":
                    receiver = client.get_input_entity(user[1])
                else:
                    receiver = InputPeerUser(user[2], user[3])
            except:
                obj = Member.Model.manager().get(username=user[0])
                obj.deleted_at = 'deleted_account'
                obj.update()
                db.commit()

            if receiver is not None:
                client.forward_messages(receiver, message_id, chat_id)
                Logs.Log(receiver.user_id, datetime.now()).save()
                db.commit()
                counter = counter + 1
                time.sleep(7)

            if counter >= cpo:
                time.sleep(60)
                counter = 0
    except ValueError:
        print(ValueError)


def get_message(member):
    msgs = ['سلام. خوبی؟ \n' \
            'ببخشید که مزاحمت میشم. من یک سایت پیدا کردم که هر محصولی که فکرشو بکنی(از شیر مرغ تا جون آدمیزاد) توش '
            'پیدا میشه\n' \
            'اگر دنبال محصولات سالم و با کیفیت خانگی و محلی هستی پیشنهاد میکنم یه سری به سایتشون بزنی\n' \
            'آدرسشون اینه: https://www.basalam.com?from=tch',

            'سلام. خوبی؟'
            'ببخشید که مزاحم میشم. من داشتم دنبال یه سری لوازم آرایشی با کیفیت و لوکس میگشتم که با باسلام آشنا شدم \n'
            'قیمت هاشون واقعا عالیه و محصولاتشون ارزش خرید بالایی داره. سایتشونم پر از کد تخفیف و کوپنه.\n'
            'لینک سایتشون رو میزارم اگر خواستی یه سری بزن.\n'
            'http://www.basalam.com/from=tch']


def update_database():
    for chat in tqdm(get_chats()):
        if not isinstance(chat, ChatForbidden) and chat.megagroup is True:
            for member in get_members(chat):
                if member.username is None:
                    member.username = "None"
                try:
                    if member.deleted is False:
                        Member.Member(member.username, member.id, member.access_hash, 'Telegram', chat.title,
                                      chat.id).save()
                        db.commit()
                except:
                    continue

    db.execute(
        "insert into Channel (channel_id, channel_title) select channel_id, channel from Member where channel_id not in (select channel_id from Channel) group by channel")
    db.commit()


client = TelegramClient(phone, api_id, api_hash)

db = Database('Social.sqlite')

Member.Model.db = db
Channel.Model.db = db

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

inp = input("Do you Want To Update Database Before start? [Y/N]:  ")
if inp.lower() == 'y':
    print("Updating Database... ")
    update_database()
    print("Database Updated... ")

chats = Channel.Channel.manager().all()
for chat in chats:
    print("chat_id: ", chat.id, " Group_title: ", chat.channel_title)

group_id = input("Enter Group_id: ")

group_id = (Channel.Channel.manager().get(id=group_id)).channel_id
members = db.execute(
    "select id,username,user_id,access_hash from Member where deleted_at isnull and channel_id = " + str(group_id))

messages = client.get_messages(1455803019, limit=10)

for message in messages:
    if isinstance(message, Message):
        print(message)

message_id = int(input("Enter Message_id: "))

forward_message(members, message_id, 1455803019, 1)

# for chat in tqdm(get_chats()):
#     if not isinstance(chat, ChatForbidden) and chat.megagroup is True:
#         for member in tqdm(get_members(chat)):
#             if member.username is None:
#                 member.username = "None"
#             try:
#                 if member.deleted is False:
#                     Member.Member(member.username, member.id, member.access_hash, 'Telegram', chat.title,
#                                   chat.id).save()
#                     db.commit()
#             except:
#                 continue


# message = client.get_messages(1455803019, 5)[0]
# forward_message(member, message, 10)
