#!/usr/bin/python2

# TeXt-Top - Google Voice Edition (no longer relies on Amazon Services)
#  Runs purely from your computer, no servers needed

# README:
# When installing pygooglevoice, you must edit the ~/.gvoice file so it contains
#  your Gmail address, password, and Google Voice number (10 digits no dashes)
#  for this program to work.

# IMPORTANT:
# When texting from the phone you choose to be your command phone, every 
#  text will be treated as a command, and they will be deleted soon after
#  being received.  This may be fixed in future versions (mostly depends on
#  Google's cooperation on making a better Voice API, or rather, making an
#  API at all).
#  Also the format for the phone you are texting from should be
#  '+10000000000', a +1 followed by your 10 digit number, NO OTHER SYMBOLS

# Dependencies:
# python2-pygooglevoice

__author__ = 'Dan Seminara'
__credits__ = {'TeXt-Top Team': [
    'Dan Daly',
    'Derek Duchesne',
    'Steven Kolln',
    'Dan Seminara']}

import os
import sys
import glob
import time
#import threading
from subprocess import Popen,PIPE
from googlevoice import Voice

current_dir = os.path.dirname(__file__)
if current_dir:
    os.chdir(current_dir)

class App:
    
    def __init__(self):
        # Configure ~/.gvoice file for this to work (or wait for prompt)
        self.voice = Voice()
        self.voice.login()
        self.extensions = {
            # File extension to search for when validating command
            '.sh': {
                # Program name to prepend to command list when executing
                # For Linux
                'linux2': None,
                # For Windows
                'win32': None
                },
            '.py': {
                'linux2': 'python2',
                'win32': 'python'
                },
            '.bat': {
                'linux2': None,
                'win32': None
                }
                # Add others as needed
            }
        # Either type in number here or set environment variable
        self.user_phone = os.environ.get('PHONE_NUMBER')
        self.command_dir = ('commands/linux', 'commands\\windows')[sys.platform == 'win32']


    def start_polling(self):
        # Threading needed later (maybe)
        self.poll_for_messages()


    def validate(self, command):
        # Debugging
        print '%s/%s.*' % (self.command_dir,command[0])
        # Checks for the existence of the command as a file (no ext)
        potentials = []
        for ext in self.extensions:
            potentials.extend(glob.glob(os.path.join(self.command_dir, '%s%s' % (command[0],ext))))
        # Perfect, found just 1
        if len(potentials) == 1:
            command[0] = potentials[0]
            return command
        print str(potentials)
        if len(potentials) > 1:
            self.error('Ambiguous Command')
        else:
            self.error('Invalid Command')
        return False


    def error(self, text):
        self.voice.send_sms(self.user_phone, text)


    def poll_for_messages(self):
        while True:
            try:
                # Checks for unread text messages not in spam
                for message in self.voice.search('is:unread in:sms -in:spam').messages:
                    # If the command phone isn't texting, ignore
                    if message.phoneNumber != self.user_phone:
                        continue
                    command = message.messageText.split(',')
                    for i,old in enumerate(command):
                        command[i] = old.strip()
                    args = self.validate(command)
                    # Prevent endless error texts, fix later
                    if not args:
                        message.delete()
                        continue
                    if self.extensions[os.path.splitext(args[0])[1]][sys.platform]:
                        args.insert(0,self.extensions[os.path.splitext(args[0])[1]][sys.platform])
                    # Debugging
                    print args
                    p = Popen(args, stdout=PIPE)
                    output,errcode = p.communicate()
                    if errcode is None:
                        errcode = 0
                    if output:
                        output = output.strip()
                        print output
                        self.voice.send_sms(self.user_phone, output)
                    else:
                        print errcode
                        if not errcode:
                            self.voice.send_sms(self.user_phone, 'Command completed successfully')
                        else:
                            self.voice.send_sms(self.user_phone, 'Error Code %s' % str(errcode))
                    message.delete()
            except:
                raise
            finally:
                # Be careful changing, don't want a captcha
                # Consider using thread timer so sleeping doesn't hog thread
                time.sleep(20)


def main():
    texttop = App()
    texttop.start_polling()

if __name__ == '__main__':
    main()
