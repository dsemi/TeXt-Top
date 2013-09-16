import os, sys
import shlex
from subprocess import Popen, PIPE


def download(user_input='',filename=''):
    user_input = sys.argv[1]
    if filename:
        filename = '-O '+filename

    command = '"%s" %s --no-check-certificate %s' % (os.path.abspath(os.path.join(os.path.dirname(__file__),'wget.exe')), filename, user_input)
    os.chdir(os.environ.get('userprofile')+'\\Downloads')
    p = Popen(shlex.split(command), stdout=PIPE)
    output,errcode = p.communicate()
    return 0


if __name__ == '__main__':
    download()
