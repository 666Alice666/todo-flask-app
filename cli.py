#!/usr/bin/env python3

import sys
import argparse
from commands import migrate, create_admin, clear_cache
from app import app  # ваше основное Flask-приложение

def main():
    parser = argparse.ArgumentParser(description="CLI for Todo Flask App")
    parser.add_argument(
        'command',
        choices=['server', 'migrate', 'create-admin', 'clear-cache'],
        help='Available commands: server, migrate, create-admin, clear-cache'
    )
    parser.add_argument('--email', help='Email for create-admin command')

    args = parser.parse_args()

    if args.command == 'server':
        app.run(host='0.0.0.0', port=5000)
    elif args.command == 'migrate':
        migrate()
    elif args.command == 'create-admin':
        if not args.email:
            print("Error: --email is required for create-admin command", file=sys.stderr)
            sys.exit(1)
        create_admin(args.email)
    elif args.command == 'clear-cache':
        clear_cache()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()