import socket
import urllib.parse
import glob
import sys
import string
import re
import time

class WebAppFuzzer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

        files = glob.glob('./fuzzdb/attack/xss/**/*.txt', recursive=True)
        self.fuzzdb = []
        for fname in files:
            f = open(fname, 'rb')
            data = f.read().decode('utf-8').splitlines()
            self.fuzzdb += data
            f.close()
        
        f = open('./http_template.txt', 'rb')
        data = f.read().decode('utf-8').replace('\n', '\r\n')
        self.http_template = string.Template(data)
        f.close()

        self.status_code = 0

    def gen_fuzz(self, index):
        return self.fuzzdb[index]

    def do_fuzz(self, fuzz):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        fuzz = urllib.parse.quote(fuzz)
        request = self.http_template.substitute(param=fuzz)
        s.send(request.encode('utf-8'))

        time.sleep(0.05)
        response = ''
        while True:
            buf = s.recv(1024).decode('utf-8')
            response += buf
            if len(buf) < 1024:
                break

        s.close()
        return response

    def is_vulnerable(self, fuzz, response):
        ptn = '[1-5][0-5][0-9]'
        match = re.search(ptn, response)
        self.status_code = int(match.group(0))
        if self.status_code >= 500:
            return True
        
        if fuzz in response:
            return True
        
        return False

    def dump(self, fuzz):
        data = str(self.status_code) + ',' + 'fuzz' + '\n'
        f = open('dump.csv', 'a')
        f.write(data)
        f.close()


def main():
    host = sys.argv[1]
    port = sys.argv[2]
    fuzzer = WebAppFuzzer(host, port)

    dump_cnt = 0
    print('%d fuzz' % len(fuzzer.fuzzdb))
    for i in range(len(fuzzer.fuzzdb)):
        fuzz = fuzzer.gen_fuzz(i)
        response = fuzzer.do_fuzz(fuzz)
        if fuzzer.is_vulnerable(fuzz, response):
            dump_cnt += 1
            fuzzer.dump(fuzz)
        sys.stdout.write('\rfuzz: %d, dumped: %d' % (i+1, dump_cnt))
        sys.stdout.flush()
    print('')


if __name__ == '__main__':
    main()
