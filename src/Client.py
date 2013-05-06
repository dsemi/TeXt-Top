#!/usr/bin/python2

import boto
import os
import re
import glob
import cPickle as pickle
from subprocess import Popen,PIPE
import thread
import time
import urllib2
import requests
import base64
import shutil
import Tkinter
import tkFileDialog
from Tkinter import Frame
from Tkinter import Label
from Tkinter import Text
from Tkinter import Entry 
from Tkinter import Button
from Tkinter import Checkbutton
from Tkinter import Listbox
from Tkinter import Scrollbar
from Tkinter import Toplevel
import Image, ImageTk

# Required packages for running from source include:
# boto
# requests
# imaging and imaging-tk

current_dir = os.path.dirname(__file__) #change directory to the current directory
if current_dir:
    os.chdir(current_dir)

class Client:
    # Initializes the Client class
    def __init__(self):
        self.amazon_access_key = ''
        self.amazon_secret_key = ''
        self.extensions = ['.sh','.py','.bat']
        self.linux_exts = [('Python file', '*.py'), ('Shell script', '*.sh')]
        self.windows_exts = [('Python file', '*.py'), ('Batch file', '*.bat')]
        self.ext_match = re.compile('(%s)$' % ('|'.join(self.extensions)))
        self.phone_match = re.compile('\+1[0-9]{10}')
        self.logged_in = False
        self.db = self.sqs = self.s3 = self.users1 = self.users2 = self.bucket = self.queue = None
        # Need if file is a Windows executable
        if os.environ.get('_MEIPASS2'):
            self.iconpath = os.path.join(os.environ.get('_MEIPASS2'), 'pics/TeXt-Top.ico')
            self.imagelogo = os.path.join(os.environ.get('_MEIPASS2'), 'pics/TeXtTopLogo2.png')
            self.imagelogosmaller = os.path.join(os.environ.get('_MEIPASS2'), 'pics/TeXtTopLogo2Smaller.png')
        else:
            self.iconpath = os.path.abspath('pics/TeXt-Top.ico') if os.name == 'nt' else '@pics/TeXt-Top-0.xbm'
            self.imagelogo = os.path.abspath('pics/TeXtTopLogo2.png')
            self.imagelogosmaller = os.path.abspath('pics/TeXtTopLogo2Smaller.png')
        self.root = Tkinter.Tk() # root is the main window of the Client
        self.root.title("TeXt-Top")
        self.root.wm_iconbitmap(self.iconpath)
        self.root.geometry("640x480")
        self.root.configure(background="black")
        self.autologin_disabled = False
        if os.name == 'posix':
            self.osversion = "linux"
        elif os.name == 'nt':
            self.osversion = "windows"
        else:
            print "OS is not supported."


    #checks if the user has a connection to the given aws service
    def check_connection(self):
        try:
            urllib2.urlopen('http://www.google.com',timeout=1)
            return True
        except urllib2.URLError:
            self.error("Error", "There is a problem with your Internet connection.", self.root, self.root)
        return False


    def initialize(self):
        if self.check_connection():
            self.db = boto.connect_dynamodb(self.amazon_access_key, self.amazon_secret_key, is_secure=True, validate_certs=False)
            self.users1 = self.db.get_table("Users1")
            self.users2 = self.db.get_table("Users2")
            self.sqs = boto.connect_sqs(self.amazon_access_key, self.amazon_secret_key, is_secure=True, validate_certs=False)
            self.s3 = boto.connect_s3(self.amazon_access_key, self.amazon_secret_key, is_secure=True, validate_certs=False)
            self.bucket = self.s3.get_bucket("text-top")
            return True
        return False


    # Draws the gui
    def gui(self):
        #draw all of the widgets
        logo = self.paint_image(self.imagelogo, 170, 30, 322, 144)
        username_label = Label(text="Username", fg="white", background="black")
        username_label.place(x=120,y=200)
        username_field = Entry(width=40)
        username_field.place(x=200, y=200)
        username_field.focus()
        password_label = Label(text="Password", fg="white", background="black")
        password_label.place(x=120,y=240)
        password_field = Entry(show="*", width=40)
        password_field.place(x=200, y=240)
        hide_check = Tkinter.IntVar()
        hide_checkbutton = Checkbutton(text="Hide window on login", selectcolor="black", background="black", foreground="white", activebackground="black", activeforeground="white", variable=hide_check)
        hide_checkbutton.place(x=160, y=360)
        auto_check = Tkinter.IntVar()
        auto_checkbutton = Checkbutton(text="Auto-login", selectcolor="black", background="black", foreground="white", activebackground="black", activeforeground="white", variable=auto_check)
        auto_checkbutton.place(x=360, y=360)
        login_button = Button(height=1, width=10, text="Login", command=lambda: self.login(username_field.get(), base64.b64encode(password_field.get()), hide_check.get(), auto_check.get()))
        login_button.place(x=220, y=280)
        register_button = Button(height=1, width=10, text="Register", command=lambda: self.register_window(username_field.get(), password_field.get()))
        register_button.place(x=340, y=280)
        
        #allow the user to hit tab to switch between entry fields and enter to login (when the password field is active)
        password_field.bind("<Return>", lambda e: self.login(username_field.get(), base64.b64encode(password_field.get()), hide_check.get(), auto_check.get()))
        username_field.bind("<Tab>", self.focus_next_window)

        #check user's preferences and mark the corresponding boxes in the gui
        preferences = self.check_preferences(hide_checkbutton, auto_checkbutton)

        if not self.db:
            if not self.initialize():
                return

        if preferences.get('autologin') and preferences.get('username') and self.check_connection() and not self.autologin_disabled:
            username = preferences.get('username')
            password = self.users1.get_item(username).get('Password','')
            self.login(username, password, hide_check.get(), 1)

    #the window that appears when a user hits the 'Register' button    
    def register_window(self, username, password): 
        #verify that the user is connected to the internet
        if not self.db:
            if not self.initialize():
                return
        if not username or not password:
            self.error("Error", "Username or password field cannot be blank.", self.root, self.root)
        elif re.search('\s', username):
            #give the user an error if their name contains spaces
            self.error("Error", "Usernames cannot contain spaces.", self.root, self.root)
        else:
            #draw the registration window
            current = Toplevel(self.root, padx="10", pady="10")
            current.focus_force()
            current.title("Registration")
            current.wm_iconbitmap(self.iconpath)
            current.geometry("+%d+%d" % (self.root.winfo_rootx()+100, self.root.winfo_rooty()+100))
            current.configure(background="black")
            Label(current, text="Your username: " + username, fg="white", bg="black", padx="5", pady="5").grid(row=0)
            Label(current, text="Your password: " + "*"*len(password), fg="white", bg="black", padx="5", pady="5").grid(row=1)
            Label(current, text="Phone number", fg="white", bg="black", padx="5", pady="5").grid(row=2)
            phoneNum = Entry(current)
            phoneNum.grid(row=2, column=1)
            Label(current, text="Register?", fg="white", bg="black", padx="5", pady="5").grid(row=3)
            Button(current, text="OK", height=1, width=10, command=lambda: self.add_user(current, username, base64.b64encode(password), phoneNum.get())).grid(row=4, column=0)
            Button(current, text="Cancel", height=1, width=10, command=lambda: current.destroy()).grid(row=4, column=1)

            
    # Creates a user account - activated when the user tries to register an account
    def add_user(self, layer, username, passwd, phone_number):
        #check if the user is connected to the internet
        if not self.db:
            if not self.initialize():
                return

        #create data for the user 
        phone_number= "+1" + re.sub('[-()]', '', phone_number)
        #verify credentials
        if not self.phone_match.match(phone_number):
            self.error("Error", "Phone numbers must be of length 10.", layer, layer)
            return

        #check to see if a user with that name exists
        try:
            self.users1.get_item(hash_key=username) 
        #if not, register them
        except:
            userData1 = {
            'Username': username,
            'Password': passwd,
            'Phone Number': phone_number,
            }
            userData2 = {
            'Phone Number': phone_number,
            'Username': username,
            }
            self.users1.new_item(username, attrs=userData1).put()
            self.users2.new_item(phone_number, attrs=userData2).put()
            with open('preferences.txt', 'wb') as f:
                pickle.dump({
                    'hide_on_login': False,
                    'autologin': False,
                    'username': username
                }, f, -1)
            os.mkdir(username)
            keys = self.bucket.get_all_keys(prefix=self.osversion + "/")
            # HEREE - Speed up?
            for key in keys:
                if os.name == 'nt':
                    self.bucket.copy_key("users/%s/%s" % (username,key.name.replace("windows/","")), "text-top", key.name)
                else:
                    self.bucket.copy_key("users/%s/%s" % (username,key.name.replace("linux/","")), "text-top", key.name)
                
            self.copy_commands(username)
            self.sqs.create_queue(username)
            self.root.focus_force()
            layer.destroy()
        #if another user with that name exists, give an error message
        else:
            self.error("Error", "A user with that name already exists.", layer, layer)


    #activated when the user hits the 'Login' button    
    def login(self, username, passwd, hide, auto):
        if not self.db:
            if not self.initialize():
                return
        try:
            credentials = self.users1.get_item(hash_key=username)
        except:
            self.error("Error", "Invalid username or password.", self.root, self.root)
        else:
            if(credentials['Password'] == passwd): #if they entered the right credentials, make a local copy of their s3 folder and let them in
                if not os.path.isdir(username):
                    os.mkdir(username)
                    self.copy_commands(username)
                self.update_preferences(hide, auto, username)
                with open('preferences.txt', 'rb') as f:
                    contents = pickle.load(f)
                self.logged_in = True
                self.autologin_disabled = False
                thread.start_new_thread(self.get_command, (username,))
                if contents.get('hide_on_login'):
                    self.root.withdraw()
                else:
                    self.main_menu(username)
            else:
                self.error("Error", "Invalid username or password.", self.root, self.root)


    def logout(self):
            self.logged_in = False
            self.autologin_disabled = True
            for widget in self.root.winfo_children():
                widget.destroy() #clear the screen
            self.gui()


    # Draws the main menu - is called every time Main Menu is navigated to
    def main_menu(self, username):
        #start checking for commands being sent by the user
        for widget in self.root.winfo_children():
            widget.destroy() #clear the screen
        #draw the widgets
        logo = self.paint_image(self.imagelogo, 170, 30, 322, 144)
        username_label = Label(text=username, fg="white", font=("AgencyFB", 14), background="black")
        username_label.place(x=310-username.__len__()*2, y=160)
        hide_window = Button(height=1, width=30, text="Hide window", command=lambda: self.root.withdraw())
        hide_window.place(x=220, y=200)
        preferences = Button(height=1, width=30, text="Preferences", command=lambda: self.preferences(username))
        preferences.place(x=220, y=240)
        commands = Button(height=1, width=30, text="Manage commands", command=lambda: self.commands(username))
        commands.place(x=220, y=280)
        logout = Button(height=1, width=30, text="Logout", command=lambda: self.logout())
        logout.place(x=220, y=320)
        quit = Button(height=1, width=30, text="Quit", command=lambda: self.root.destroy())
        quit.place(x=220, y=360)
        phone_label = Label(text="Text 908-442-7716!", bg="black", fg="white", font=("AgencyFB", 14, "italic"))
        phone_label.place(x=240, y=400)

        
    # Draws the preferences screen
    def preferences(self, username):
        for widget in self.root.winfo_children():
            widget.destroy() #clear the screen
        #draw the widgets
        logo = self.paint_image(self.imagelogosmaller, 25, 25, 129, 58)
        preferences_label = Label(text="☃Preferences☃", fg="white", font=("AgencyFB", 32), bg="black")
        preferences_label.place(x=180, y=100)
        change_password_label = Label(text="Change password", fg="white", bg="black")
        change_password_label.place(x=280, y=200)
        change_password = Text(width=30, height=1)
        change_password = Entry(show="*", width=40)
        change_password.place(x=210, y=240)
        hide_check = Tkinter.IntVar()
        hide_checkbutton = Checkbutton(text="Hide window on login", selectcolor="black", background="black", foreground="white", activebackground="black", activeforeground="white", variable=hide_check)
        hide_checkbutton.place(x=250, y=290)
        auto_check = Tkinter.IntVar()
        auto_checkbutton = Checkbutton(text="Auto-login", selectcolor="black", background="black", foreground="white", activebackground="black", activeforeground="white", variable=auto_check)
        auto_checkbutton.place(x=250, y=340)
        save = Button(height=1, width=30, text="Save changes", command=lambda: self.save_preferences(username, change_password.get(), hide_check.get(), auto_check.get()))
        save.place(x=220, y=400)
        #update checkboxes
        self.check_preferences(hide_checkbutton, auto_checkbutton)

        
    # Draws the command management screen
    def commands(self, username):
        for widget in self.root.winfo_children():
            widget.destroy() #clear the screen
        #draw the widgets
        logo = self.paint_image(self.imagelogosmaller, 25, 25, 129, 58)
        command_label = Label(text="☃Commands☃", fg="white", font=("AgencyFB", 32), bg="black")
        command_label.place(x=180, y=100)
        command_box = Listbox(height = 7, width = 30, font=("AgencyFB", 18), fg="white", bg="black")
        command_box.place(x=70, y=200)
        add = Button(height=1, width=10, text="Add...", command=lambda: self.add_script(username, command_box))
        add.place(x=500, y=240)
        delete = Button(height=1, width=10, text="Delete", command=lambda: self.delete_script(username, command_box, command_box.get("active")))
        delete.place(x=500, y=280)
        back = Button(height=1, width=10, text="Return", command=lambda: self.main_menu(username))
        back.place(x=500, y=320)
        phone_label = Label(text="Text 908-442-7716!", bg="black", fg="white", font=("AgencyFB", 14, "italic"))
        phone_label.place(x=240, y=400)
                
        keys = sorted(os.listdir(username))
        for key in keys:
            if self.ext_match.search(key):
                command_box.insert("end", os.path.splitext(key)[0])

                
    #save's the user's preferences to 'preferences.txt'
    def save_preferences(self, username, newpass, hide, auto):
        #verify the user's connection to the internet
        if not self.db:
            if not self.initialize():
                return
        #save the user's preferences
        item = self.users1.get_item(hash_key=username)
        if len(newpass) > 0:
            item.put_attribute("Password", base64.b64encode(newpass))
        item.save()
        self.update_preferences(hide, auto, username)
        self.main_menu(username)        
      
    
    #adds a new command to the user's s3 folder and their local folder    
    def add_script(self, username, listbox):
        #verify the user's connection to the internet
        if not self.db:
            if not self.initialize():
                return
        # OS Check
        if os.name == 'posix':
            # Account for user pressing cancel
            script = tkFileDialog.askopenfilenames(title="Select script", filetypes=self.linux_exts)
            #Possible conflicting line of code.
            script=script[0]
        elif os.name == 'nt':
            script = tkFileDialog.askopenfilenames(title="Select script", filetypes=self.windows_exts).strip('{}')
        else:
            print 'OS not supported'
        _,exten = os.path.splitext(script)
        if not len(script) == 0:
            script_name = script.rsplit('/', 1)[1].strip('}')
            if self.bucket.get_key("users/%s/%s" % (username,script_name)) is None:
                k = self.bucket.new_key("users/%s/%s" % (username,script_name))
                k.set_contents_from_filename(script)
                listbox.insert("end", script_name[:-len(exten)])
                shutil.copy(script, username)
            else:
                self.error("Error", "A command by that name already exists.", self.root, self.root)
    
    
    #deletes a script from the user's command menu, their s3 bucket, and their local commands
    def delete_script(self, username, listbox, active):
        #verify the user's connection to the internet
        if not self.db:
            if not self.initialize():
                return

        listbox.delete("active")
        self.bucket.delete_keys(['users/%s/%s%s' % (username,active,ext) for ext in self.extensions])
        for f in glob.glob('%s/%s.*' % (username,active)):
            os.remove(f)


    #allows you to put images in a window    
    def paint_image(self, filename, x, y, width, height):
        image = Image.open(filename)
        photo = ImageTk.PhotoImage(image)
        label = Label(image=photo)
        label.image = photo
        label.pack()
        label.place(x=x, y=y, width=width, height=height)
        return label


    #closes the active window and gives focus to the parent window
    def close_focus(self, layer, parent):
        parent.focus_force()
        layer.destroy()


    #needed to tab between text fields
    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()
        return("break")


    #activated once the user logs in, checks for commands being sent through to the user's queue and activates them
    def get_command(self, username):
        while not self.sqs:
            pass
        queue = self.sqs.get_queue(username)
        while True:
            try:
                while not self.sqs:
                    time.sleep(5)
                message = queue.read()
                if not message:
                    time.sleep(15)
                    if not self.logged_in:
                        thread.exit()
                    continue
                queue.delete_message(message)
                command = message.get_body()
                args = command.split(",")
                if os.name == 'nt':
                    separator = '\\'
                else:
                    separator = '/'
                
                files = os.listdir(username)

                command_names = {}
                for i in files:
                    temp1,temp2 = os.path.splitext(i)
                    command_names[temp1] = temp2

                if args[0] in command_names:
                    ext = command_names[args[0]]
                    args[0] = '%s%s%s%s' % (username,separator,args[0],ext)
                    if ext == '.py':
                        if os.name == 'nt':
                            args = ['python'] + args
                        else:
                            args = ['python2'] + args
                print args
                p = Popen(args, stdout=PIPE)
                output,errcode = p.communicate()
                if errcode is None:
                    errcode = 0
                phone = self.users1.get_item(username)['Phone Number']
                if output:
                    output = output.strip()
                    print output
                    requests.post("http://text-top.elasticbeanstalk.com/response", params={"output":output, "error code":errcode, "phone":phone})
                else:
                    print errcode
                    requests.post("http://text-top.elasticbeanstalk.com/response", params={"error code":errcode, "phone":phone})
                    
            except:
                raise


    #verifies that a user's preferences file exists. if it doesn't, it is created. the checkboxes for those preferences are also filled in
    def check_preferences(self, hide_checkbutton, auto_checkbutton):
        try:
            with open('preferences.txt'): pass
        except IOError:
            with open('preferences.txt', 'wb') as f:
                pickle.dump({
                    'hide_on_login': False,
                    'autologin': False
                }, f, -1)
        with open('preferences.txt', 'rb') as f:
            contents = pickle.load(f)
        if contents.get('hide_on_login'): # Hide window on login
            hide_checkbutton.select()
        if contents.get('autologin'): # Autologin
            auto_checkbutton.select()
        return contents


    #updates the user's preferences in the preferences.txt file
    def update_preferences(self, hide, auto, username):
        with open('preferences.txt', 'wb') as f:
            pickle.dump({
                'hide_on_login': bool(hide),
                'autologin': bool(auto),
                'username': str(username)
            }, f, -1)

            
    #makes a local copy of the user's commands mirror those in the user's s3 bucket
    def copy_commands(self, username):
        keys = self.bucket.get_all_keys(prefix="users/" + username)
        for key in keys:
            if key.name.endswith('/'):
                continue
            key.get_contents_to_filename(key.name[6:])
        if os.name == 'posix':
            os.system('chmod +x %s/*.sh' % username)


    #displays an error message to the user        
    def error(self, title, label_text, parent, focus):
        error = Toplevel(parent, padx="10", pady="10")
        error.focus_force()
        error.title(title)
        error.wm_iconbitmap(self.iconpath)
        error.geometry("+%d+%d" % (self.root.winfo_rootx()+10, self.root.winfo_rooty()+10))
        error.configure(background="black")
        Label(error, text=label_text, fg="white", bg="black", padx="5", pady="5").grid(row=0)
        Button(error, text="OK", height=1, width=10, command=lambda: self.close_focus(error, focus)).grid(row=1)


#runs the GUI
def main():
    client = Client()
    client.gui()
    client.root.mainloop()


if __name__ == '__main__':
    main()
