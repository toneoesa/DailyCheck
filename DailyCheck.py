from random import randint
import argparse
from time import asctime, sleep
from check import check
from LogGroup import LogGroup

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto Daily Check Script')
    parser.add_argument('-n', '--now', default=False, action='store_true', help='Do not delay')
    parser.add_argument('-d', '--dry', default=False, action='store_true', help='Dry run, no real check')
    parser.add_argument('-s', '--silent', default=False, action='store_true', help='Do not report result to DingDing')
    parser.add_argument('-f', '--file', default='idfile.txt', action='store',
                        help='A file with id(s), password(s) (and ding token, secret)')
    parser.add_argument('-i', '--id', default=None, action='store', help='Specify a id')
    parser.add_argument('-p', '--pwd', default=None, action='store', help='Specify a password')
    parser.add_argument('-l', '--logfile', default='log.txt', action='store', help='File to append log')
    parser.add_argument('-S', '--sleep', default=600, type=int, action='store', help='Sleep seconds before work')
    parser.add_argument('-t', '--time', default=600, type=int, action='store',
                        help='Choose time points randomly in during this time')
    args = parser.parse_args().__dict__

    access_token = ''
    secret = ''
    ids = []
    if args['file'] is not None:
        try:
            with open(args['file'], 'r', encoding='utf-8') as id_file:
                for line in id_file:
                    if len(line.replace('\n', '')) == 0 or line[0] == '#':
                        continue
                    if line[0] == '@':
                        access_token, secret = line[1:].split()[:2]
                    else:
                        info = line.split()[:3]
                        ids.append(info)
        except:
            pass

    if args['id'] is not None and args['pwd'] is not None:
        ids.append([args['id'], args['pwd'], 'TempUser'])

    if len(ids) == 0:
        print('Specify a file or a pair of id and pwd')
        exit(2)

    time_max_delay = int(args['time'] / len(ids)) + 1
    log_group = LogGroup(print='print', file='write_now',
                         ding='ding_together' if not args['silent'] and access_token and secret else 'nul')
    log_group.set_path('file', args['logfile'])
    log_group.set_ding(access_token, secret)
    log_group.write('From Daily Check:', 'ding')
    log_group.write(f'{asctime()}')

    if not args['now']:
        sleep(args['sleep'])

    for id, pwd, name in ids:
        if not args['now']:
            sleep(randint(1, time_max_delay))
        log_group.write(f'  {asctime()}')
        log_group.write(f'    {id} {name}')
        if not args['dry']:
            msg = check(id, pwd)
            log_group.write(f"    {msg['Info']}")
        else:
            log_group.write(f'    Dry Run')

    log_group.write('Check all done')
    log_group.write('')
    log_group.execute()
