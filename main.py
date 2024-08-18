import argparse
from psycopg2 import connect, OperationalError
from common.db_settings import db_settings
from common.create_database import create_database, create_tables
from user import user_menu
from message import message_menu


def main_menu():
    # Główny parser argumentów
    parser = argparse.ArgumentParser(description="Main menu for management system")
    subparsers = parser.add_subparsers(dest='command', help='Choose user or message management')

    # Parser dla zarządzania użytkownikami
    user_parser = subparsers.add_parser('user', help='User management')
    user_parser.add_argument("-u", "--username", help="username")
    user_parser.add_argument("-p", "--password", help="password (min 8 characters)")
    user_parser.add_argument("-nu", "--new_username", help="new username")
    user_parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
    user_parser.add_argument("-l", "--list", help="list all users", action="store_true")
    user_parser.add_argument("-d", "--delete", help="delete user", action="store_true")
    user_parser.add_argument("-e", "--edit", help="edit user", action="store_true")

    # Parser dla zarządzania wiadomościami
    message_parser = subparsers.add_parser('message', help='Message management')
    message_parser.add_argument("-u", "--username", help="username")
    message_parser.add_argument("-p", "--password", help="password (min 8 characters)")
    message_parser.add_argument("-l", "--list", help="list all messages", action="store_true")
    message_parser.add_argument("-t", "--to", help="recipient username")
    message_parser.add_argument("-s", "--send", help="text message to send")
    args = parser.parse_args()

    create_database()
    create_tables()

    try:
        conn = connect(**db_settings)
        conn.autocommit = True
        cursor = conn.cursor()

        if args.command == 'user':
            user_menu(cursor, args)
        elif args.command == 'message':
            message_menu(cursor, args)
        else:
            print("Please choose 'user' or 'message' and provide the required arguments.")
            parser.print_help()

        conn.close()
    except OperationalError as e:
        print("Connection failed: ", e)


if __name__ == "__main__":
    main_menu()
