import argparse
import os
import shutil
import time
import pathlib


class IDFile:
    def __init__(self, filename):
        self.filename = filename
        self.users = []
        self.access_token = ''
        self.secret = ''
        self.read()

    def read(self):
        if os.path.isfile(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as id_file:
                for line in id_file:
                    if len(line) == 0:
                        continue
                    if line[0] == '@':
                        self.access_token, self.secret = line[1:].split()[:2]
                    elif line[0] == '#':
                        id, pwd, name = line[1:].split()[:3]
                        self.users.append({
                            'id': id,
                            'pwd': pwd,
                            'name': name,
                            'enable': False
                        })
                    else:
                        id, pwd, name = line.split()[:3]
                        self.users.append({
                            'id': id,
                            'pwd': pwd,
                            'name': name,
                            'enable': True
                        })
        else:
            os.mknod(self.filename)

    def write(self, backup=False):
        if backup:
            src_path = pathlib.Path(self.filename)
            dst_path = src_path.cwd() / f"{self.filename}.{time.asctime().replace(' ', '-').replace(':', '')}"
            shutil.copyfile(src_path, dst_path)
        with open(self.filename, 'w', encoding='utf-8') as id_file:
            id_file.write(f"@ {self.access_token} {self.secret}\n")
            for user in self.users:
                if not user['enable']:
                    id_file.write('# ')
                id_file.write(f"{user['id']} {user['pwd']} {user['name']}\n")

    def list(self):
        for user in self.users:
            print(f"{'Y ' if user['enable'] else '  '} {user['id']} {user['pwd']} {user['name']}")

    def find(self, id='', name=''):
        if id:
            for idx, user in enumerate(self.users):
                if user['id'] == id:
                    return idx
        if name:
            for idx, user in enumerate(self.users):
                if user['name'] == name:
                    return idx
        return None

    def change_able(self, id='', name='', enable=True):
        idx = self.find(id, name)
        if idx is not None:
            self.users[idx]['enable'] = enable
            return True
        else:
            return False

    def add(self, id, pwd, name, enable=True):
        if self.find(id, name) is None:
            self.users.append({
                'id': id,
                'pwd': pwd,
                'name': name,
                'enable': enable
            })
            return True
        else:
            return False

    def modify(self, find_id='', find_name='', id='', pwd='', name=''):
        idx = None
        if find_id:
            idx = self.find(id=find_id)
        elif find_name:
            idx = self.find(name=find_name)
        if idx is not None:
            if id:
                self.users[idx]['id'] = id
            if pwd:
                self.users[idx]['pwd'] = pwd
            if name:
                self.users[idx]['name'] = name
            return True
        else:
            return False

    def modify_token(self, access_token='', secret=''):
        if access_token:
            self.access_token = access_token
        if secret:
            self.secret = secret


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto Daily Check Script CLI')
    parser.add_argument('-f', '--file', default='idfile.txt', action='store',
                        help='A file with id(s) and password(s)')
    parser.add_argument('-l', '--list', default=False, action='store_true', help='List all users')
    parser.add_argument('-S', '--Show', default=False, action='store_true', help='Show ding token and secret')
    parser.add_argument('-a', '--add', default=False, action='store_true', help='Add a user')
    parser.add_argument('-e', '--enable', default=False, action='store_true', help='Enable a user')
    parser.add_argument('-d', '--disable', default=False, action='store_true', help='Disable a user')
    parser.add_argument('-m', '--modify', default=None, choices=['id', 'name'], action='store',
                        help='Modify a user info (Specify which used to find a user)')
    parser.add_argument('-D', '--Ding', default=False, action='store_true',
                        help='Set or Modify Ding API token and(or) secret')
    parser.add_argument('-i', '--id', default=None, action='store', help='User id')
    parser.add_argument('-p', '--pwd', default=None, action='store', help='User password')
    parser.add_argument('-n', '--name', default=None, action='store', help='User name (Without space)')
    parser.add_argument('-t', '--token', default=None, action='store', help='Access token for DingDing')
    parser.add_argument('-s', '--secret', default=None, action='store', help='Secret for DingDing')
    args = parser.parse_args().__dict__

    id_file = IDFile(args['file'])

    if args['list']:
        id_file.list()
    elif args['Show']:
        print('Access Token :', id_file.access_token)
        print('Secret       :', id_file.secret)
    elif args['enable'] or args['disable']:
        if args['enable'] and args['disable']:
            print('What did you do???')
        else:
            enable = args['enable']
            if args['id']:
                if id_file.change_able(id=args['id'], enable=enable):
                    id_file.write()
                else:
                    print('The user id does not exist')
            elif args['name'] is not None:
                if id_file.change_able(name=args['name'], enable=enable):
                    id_file.write()
                else:
                    print('The user name does not exist')
            else:
                print('Specify either a id or a name')
    elif args['add']:
        if args['id'] and args['pwd'] and args['name']:
            if id_file.add(args['id'], args['pwd'], args['name'], enable=True):
                id_file.write()
            else:
                print('The user id or name is exist')
        else:
            print('Specify id, password and name')
    elif args['modify']:
        if args['modify'] == 'id' and args['id']:
            if args['name'] or args['pwd']:
                if id_file.modify(find_id=args['id'], pwd=args['pwd'], name=args['name']):
                    id_file.write(backup=True)
                else:
                    print('The user id does not exist')
            else:
                print('Specify the user info')
        elif args['modify'] == 'name' and args['name']:
            if args['id'] or args['pwd']:
                if id_file.modify(find_name=args['name'], id=args['id'], pwd=args['pwd']):
                    id_file.write(backup=True)
                else:
                    print('The user name does not exist')
            else:
                print('Specify the user info')
        else:
            print('Specify the user info')
    elif args['Ding']:
        if args['token'] or args['secret']:
            id_file.modify_token(args['token'], args['secret'])
            id_file.write(backup=True)
        else:
            print('Specify either a token or a secret')
