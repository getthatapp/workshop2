from common.crypto import check_password
from models.message import Message
from models.user import User


def print_user_messages(cursor, user):
    messages = Message.load_all_messages(user.id)
    for message in messages:
        from_user = User.load_user_by_id(message.from_id)
        print(20 * "-")
        if from_user:
            print(f"from: {from_user.username}")
        else:
            print("from: [Unknown User]")
        print(f"date: {message.creation_date}")
        print(message.text)
        print(20 * "-")


def send_message(cursor, from_id, recipient_name, text):
    if len(text) > 255:
        print("Message is too long!")
        return
    to_user = User.load_user_by_username(recipient_name)
    if to_user:
        message = Message(from_id, to_user.id, text=text)
        message.save_to_db()
        print("Message sent!")
    else:
        print("Message not sent, recipient does not exist")


def message_menu(cursor, args):

    if args.username and args.password:
        user = User.load_user_by_username(args.username)
        if user and check_password(args.password, user.hashed_password):
            if args.list:
                print_user_messages(cursor, user)
            elif args.to and args.send:
                send_message(cursor, user.id, args.to, args.send)
            else:
                print("No valid operation provided")
        else:
            print("Incorrect password or user does not exist!")
    else:
        print("Username and password are required")
