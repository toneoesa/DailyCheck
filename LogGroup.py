import time

from DingMessage import DingMessage


class LogGroup:
    def __init__(self, **kwargs):
        self.secret = None
        self.access_token = None
        self._logs_content = {}
        self._logs_mode = {}
        self._logs_file = {}
        for log, mode in kwargs.items():
            self._logs_content[log] = ''
            self._logs_mode[log] = mode

    def set_path(self, log_name, file_name):
        self._logs_file[log_name] = file_name

    def set_ding(self, access_token, secret):
        self.access_token = access_token
        self.secret = secret

    def _write(self, log_name, content):
        mode = self._logs_mode[log_name]
        self._logs_content[log_name] += content
        if mode == 'print':
            print(content, end='')
        elif mode == 'write_now':
            with open(self._logs_file[log_name], 'a', encoding='utf-8') as file:
                file.write(content)
        elif mode == 'write_together':
            pass
        elif mode == 'ding_together':
            pass
        elif mode == 'nul':
            pass

    def write(self, content, log_name=None, endline=True):
        if endline:
            content += '\n'
        if log_name is not None:
            self._write(log_name, content)
        else:
            for log in self._logs_content.keys():
                self._write(log, content)

    def get(self, log_name):
        return self._logs_content[log_name]

    def _execute(self, log_name):
        mode = self._logs_mode[log_name]
        if mode == 'print':
            pass
        elif mode == 'write_now':
            pass
        elif mode == 'write_together':
            with open(self._logs_file[log_name], 'a', encoding='utf-8') as file:
                file.write(self._logs_content[log_name])
        elif mode == 'ding_together':
            DingMessage(self._logs_content[log_name], self.access_token, self.secret)
        elif mode == 'nul':
            pass

    def execute(self, log_name=None):
        if log_name is not None:
            self._execute(log_name)
        else:
            for log in self._logs_content.keys():
                self._execute(log)


if __name__ == '__main__':
    with open('ids.txt', 'r', encoding='utf-8') as file:
        line0 = file.readline()
        access_token, secret = line0[1:].split()[:2]
    log_group = LogGroup(print='print', file='write_now', ding='ding_together')
    log_group.set_path('file', 'test.txt')
    log_group.set_ding(access_token, secret)
    log_group.write(f'Test at {time.asctime()}')
    log_group.execute()
