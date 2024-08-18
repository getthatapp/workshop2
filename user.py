from psycopg2.errors import UniqueViolation
from common.crypto import check_password
from models.user import User


def edit_user(cursor, username, password, new_password=None, new_username=None):
    user = User.load_user_by_username(username)
    if not user:
        print("User does not exist!")
        return

    if not check_password(password, user.hashed_password):
        print("Incorrect password")
        return

    if new_username:
        if User.load_user_by_username(new_username):
            print(f"Username '{new_username} is already taken")
            return
        user.username = new_username

    if new_password:
        if len(new_password) < 8:
            print("Password is too short! Minimum 8 characters required.")
            return
        user.password = new_password

    user.save_to_db()
    print("User updated successfully")


def delete_user(cursor, username, password):
    user = User.load_user_by_username(username)
    if not user:
        print("User not found!")
    elif check_password(password, user.hashed_password):
        user.delete_user()
        print("User deleted.")
    else:
        print("Incorrect password")


def create_user(cursor, username, password):
    if len(password) < 8:
        print("Password is too short! Minimum 8 characters required.")
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db()
            print("User created.")
        except UniqueViolation as e:
            print("Error creating user", e)


def list_users(cursor):
    users = User.load_all_users()
    for user in users:
        print(user.username)


def user_menu(cursor, args):
    if args.list:
        list_users(cursor)
    elif args.username and args.password and args.edit and (args.new_pass or args.new_username):
        edit_user(cursor, args.username, args.password, args.new_pass, args.new_username)
    elif args.username and args.password and args.delete:
        delete_user(cursor, args.username, args.password)
    elif args.username and args.password:
        create_user(cursor, args.username, args.password)
    else:
        print("No valid operation provided")
