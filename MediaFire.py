import os, re, shutil, sys, time, tempfile
try:
    import requests
except:
    os.system('pip install requests')

try:
    import six
except:
    os.system('pip install six')

try:
    import tqdm
except:
    os.system('pip install tqdm')

CHUNK_SIZE = 524288

os.system('clear')
def banner():
    print("""
\033[1;36m     ███▄ ▄███▓▓█████ ▓█████▄  ██▓ ▄▄▄           █████▒██▓ ██▀███  ▓█████
\033[1;36m     ▓██▒▀█▀ ██▒▓█   ▀ ▒██▀ ██▌▓██▒▒████▄       ▓██   ▒▓██▒▓██ ▒ ██▒▓█   ▀
\033[1;34m     ▓██    ▓██░▒███   ░██   █▌▒██▒▒██  ▀█▄     ▒████ ░▒██▒▓██ ░▄█ ▒▒███
\033[1;34m     ▒██    ▒██ ▒▓█  ▄ ░▓█▄   ▌░██░░██▄▄▄▄██    ░▓█▒  ░░██░▒██▀▀█▄  ▒▓█  ▄
\033[1;92m     ▒██▒   ░██▒░▒████▒░▒████▓ ░██░ ▓█   ▓██▒   ░▒█░   ░██░░██▓ ▒██▒░▒████▒
\033[1;97m●●●●●●●●●●●●●●●●●●●●\033[1;92m<><>\033[1;97m●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
\033[1;97m	           Pembuat Tools\033[1;97m: \033[1;92mARIEL SANDY PERMANA
\033[1;97m	           Youtube\033[1;97m: \033[1;92mAriel 69 Channel
\033[1;97m	           Git Hub\033[1;97m: \033[1;92mhttps://github.com/Kingblack44
\033[1;97m●●●●●●●●●●●●●●●●●●●●\033[1;92m<><>\033[1;97m●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●""")

def extractDownloadLink(contents):
    for line in contents.splitlines():
        m = re.search('href="(https://download[^"]+)', line)
        if m:
            return m.groups()[0]


def download(url, output, quiet):
    url_origin = url
    sess = requests.session()
    while 1:
        res = sess.get(url, stream=True)
        if 'Content-Disposition' in res.headers:
            break
        url = extractDownloadLink(res.text)
        if url is None:
            print(('Permission denied: %s' % url_origin), file=(sys.stderr))
            print("Maybe you need to change permission over 'Anyone with the link'?",
              file=(sys.stderr))
            return

    if output is None:
        m = re.search('filename="(.*)"', res.headers['Content-Disposition'])
        output = m.groups()[0]
    output_is_path = isinstance(output, six.string_types)
    if not quiet:
        print('Downloading...', file=(sys.stderr))
        print('From:', url_origin, file=(sys.stderr))
        print('To:',
          (osp.abspath(output) if output_is_path else output),
          file=(sys.stderr))
    if output_is_path:
        tmp_file = tempfile.mktemp(suffix=(tempfile.template),
          prefix=(osp.basename(output)),
          dir=(osp.dirname(output)))
        f = open(tmp_file, 'wb')
    else:
        tmp_file = None
        f = output
    try:
        try:
            total = res.headers.get('Content-Length')
            if total is not None:
                total = int(total)
            if not quiet:
                pbar = tqdm.tqdm(total=total, unit='B', unit_scale=True)
            for chunk in res.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
                if not quiet:
                    pbar.update(len(chunk))

            if not quiet:
                pbar.close()
            if tmp_file:
                f.close()
                shutil.move(tmp_file, output)
        except IOError as e:
            try:
                print(e, file=(sys.stderr))
                return
            finally:
                e = None
                del e

    finally:
        try:
            if tmp_file:
                os.remove(tmp_file)
        except OSError:
            pass

    return output


if __name__ == '__main__':
    banner()
try:
    url = input('\x1b[0;37m┌─[\x1b[31;1m Input Link Mediafire \x1b[0;37m]\n\x1b[0;37m└─[\x1b[31;1m$\x1b[0;37m]> \x1b[36;1m')
    print('\x1b[0;37m')
    download(url, output=None, quiet=False)
except IndexError:
    print('\n\x1b[31;1m[\x1b[0;37m!\x1b[31;1m] \x1b[0;37mthere is an error')
    sys.exit()
except KeyboardInterrupt:
    print('\n\x1b[31m[\x1b[0m!\x1b[31m]\x1b[0m ctrl+c detected')
    print('\x1b[31m[\x1b[0m!\x1b[31m]\x1b[0m trying to exit')
    time.sleep(3)
    sys.exit()
except EOFError:
    print('\n\n\x1b[31m[\x1b[0m!\x1b[31m]\x1b[0m ctrl+d detected')
    print('\x1b[31m[\x1b[0m!\x1b[31m]\x1b[0m trying to exit')
    time.sleep(3)
    sys.exit()
except requests.exceptions.MissingSchema:
    print('\n\x1b[31m[\x1b[0m!\x1b[31m]\x1b[0m invalid url')
    print('\x1b[31m[\x1b[0m!\x1b[31m]\x1b[0m trying to exit')
    time.sleep(3)
    sys.exit()
