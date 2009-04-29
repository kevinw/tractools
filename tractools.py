'''
tools for interacting with trac
'''

import sys
import os.path
import subprocess
import webbrowser

DEFAULT_TRAC = 'http://mini/cgi-bin'
svn_trac_map = {}
REPOSITORY_ROOT = 'Repository Root'

def parse_svninfo(stdout):
    '''
    returns a mapping for the parsed output of a successful 'svn info'
    '''

    map = {}
    for line in stdout.split('\n'):
        line = line.strip()
        if not line:
            continue

        i = line.index(':')
        key, value = line[:i], line[i+2:]
        map[key] = value

    return map

def relative_file_url(svninfo):
    url, root = svninfo['URL'], svninfo[REPOSITORY_ROOT]
    assert url.startswith(root)
    return url[len(root):]

def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = proc.communicate()
    if proc.returncode:
        raise Exception('process returned %r: %r' % proc.returncode, cmd)

    return stdout

def open_in_browser(filename):
    if not os.path.isfile(filename):
        error('not a file: %r', filename)

    info = parse_svninfo(run('svn info %s' % filename))
    url = svn_trac_map.get(info[REPOSITORY_ROOT], DEFAULT_TRAC) + '/browser' + relative_file_url(info)

    #webbrowser.open(url)
    os.startfile(url)



def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()

    filename = args[0]
    open_in_browser(filename)

def usage():
    error('Usage: python trac.py [file]')

def error(msg, *args):
    print >> sys.stderr, msg % args
    sys.exit(1)

if __name__ == '__main__':
    main()
