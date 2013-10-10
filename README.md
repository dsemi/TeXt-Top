<pre>
///////////////////////////////////////////////////////////
 /////////        //     //       /////////                
    //             //   //           //                         
    //     ////     // //     //     //    /////    /////   
    //    //  //     //     //////   //   //   //   //  //  
    //   ////////   // //     //     //  //     //  //   // 
    //    //       //   //    //     //   //   //   //  //  
    //     /////  //     //   //     //    /////    ////    
/////////////////////////////////////////////////// // /////     
                                                    //      
                                                    // 
</pre>

## Twilio:

Thank you for downloading TeXt-Top, a program that allows you to text commands to your computer!

### Dependencies:

Linux:
- Python 2
- python-boto
- python-requests
- python-tk
- python-imaging-tk
- wget

Windows:
- Python 2 (32-bit version)
- pywin32 (32-bit version)
- Python VideoCapture

===================
Starting the program:
===================
To run TeXt-Top, simply double-click on TeXt-Top.exe (if you've downloaded the Windows build) or run the Python script TeXt-Top.py (if you've downloaded the Linux build).

======================
Navigating the interface:
======================
After running TeXt-Top, you'll be confronted with a login screen which requires you to enter a username and password.  If you're new to using the program, after typing in your credentials, click the 'Register' button and you'll be asked to provide your phone number. Once you've registered, you can then press the 'Login' button to be able to start texting commands to your computer. You'll notice checkboxes for 'Hide window on login' and 'Auto-login' at the bottom of the screen, which become active after logging in. 
*Note: After hiding the window, there is no way to close the program except by going into the task manager and ending the process.  If both hide window and auto-login are selected, there will be no way to access TeXt-Top's menu options.  A simple way to fix this is to delete the preferences.txt file in the folder where TeXt-Top is located, which will undo these preferences.

Once logged-in, you'll come to a menu with a variety of options:

'Hide window' -  Hides the window for the current session without saving the hide window option as a preference. 
'Preferences' -  Brings you to a separate screen where you have the option to enable the 'Hide window on login' and 'Auto-login' preferences as well as the ability to change your password by entering a new one in the text field. After you've finished choosing your preferences, click 'Save changes' and you'll be returned to the main menu.

'Manage commands' - Brings you to a separate screen which displays a list of all of the commands enabled for your account. Clicking on a command highlights it. You can traverse through the list by either scrolling with your mouse-wheel or pressing the arrow keys.  Once you've selected a command, you can delete it by hitting the 'Delete' button. By pressing the 'Add...' button, you'll be presented 
with a navigation menu where you can select Python scripts and either Batch files on Windows or Shell scripts on Linux to add to your account. Once you've added a command, it should appear in the commands box with the rest of the list of commands. Clicking on the 'Return' button will bring you back to the main menu.

'Logout' - Logs you out of your account without closing the program.

'Quit' - Closes the program.

==================
Texting a command:
==================
To have a command activate on your computer, text the number that is displayed on the main menu once you log in and type the name of the command you would like to execute. Some commands take arguments in addition to their name. When texting a command, you put the name of the command first and then the arguments separated by commas. For instance, 'open file' takes one argument which is the name of the file you would like to open. So, when using that command, you would text 'open file,example.txt'.  You will notice that a number of default commands come with TeXt-Top. Their names and instructions are as follows:

Windows:
----------------
1. batman - Description: Changes your desktop background to an ascii batman image, Arguments: None 
2. capture - Description: Takes a picture using your webcam and sends it to a recipient, Arguments: The email address of the recipient
3. download - Description: Downloads the file specified, Arguments: The url of the file you wish to download
4. get dir - Description: Texts you back the directory of the file you specify, Arguments: The name of the file you would like to search for
5. get ip - Description: Texts you back the IP address of your computer, Arguments: None
6. lock screen - Description: Locks your screen, Arguments: None
7. restart - Description: Restarts your computer, Arguments: None
8. send mail - Description: Sends an email remotely, Arguments: The recipient's email address, the title of your email, the file you would like to attach, the subject of the email, the name of the sender
9. shutdown - Description: Shuts down your computer, Arguments: None

Linux:
-----------
1. download - Description: Downloads the file specified, Arguments: The url of the file you wish to download
2. find file - Description: Texts you back the directory of the file you specify, Arguments: The name of the file you would like to search for
3. get ip - Description: Texts you back the IP address of your computer, Arguments: None
4. lock - Description: Locks your screen, Arguments: None
5. restart - Description: Restarts your computer, Arguments: None
6. send mail - Description: Sends an email remotely, Arguments: The recipient's email address, the title of your email, the file you would like to attach, the subject of the email, the name of the sender
7. shutdown - Description: Shuts down your computer, Arguments: None
8. unlock - Description: Unlocks your locked computer, Arguments: None

===================
Creating a command:
===================
You can write your own commands to be used by TeXt-Top in the form of either a Python script, Shell script (Linux-only), or Batch script (Windows-only). When writing your script, here are some general guidelines to keep in mind:

- The name of the script (minus the extension) will be the command name that you text.
- The arguments of your script become the comma-separated arguments when you text your command.
- Any printed statements in your code will be echoed as a text to the user, enabling you to customize the feedback to your phone.
- The exit status of the program determines the success/failure text that is sent back to the user.

Have fun!

==============
## Google Voice Edition

Thank you for downloading TeXt-Top, a program that allows you to text commands to your computer!

### Dependencies:
A Google Voice number; it's free and easy to set up, and you'll have your own personal command receiver

Linux:
- Python 2
- python2-pygooglevoice
- wget

Windows:  
(May have to edit C:\Python27\site-packages\googlevoice\settings.py and change LOGIN to 'https://accounts.google.com/ServiceLogin?service=code&ltmpl=phosting&continue=http%3A%2F%2Fcode.google.com%2Fp%2Fpygooglevoice%2Fissues%2Fdetail%3Fid%3D64&followup=http%3A%2F%2Fcode.google.com%2Fp%2Fpygooglevoice%2Fissues%2Fdetail%3Fid%3D64'
see [here](https://code.google.com/p/pygooglevoice/issues/detail?id=64))
- Python 2
- python2-pygooglevoice


#### Important:
When installing pygooglevoice, be sure to edit the ~/.gvoice file so it contains your Gmail address, password (I know, looking for fix), and Google Voice number (10 digits no dashes).  If you decide you want to leave the password blank, you will be prompted upon launching the program.

You also must either make an environment variable PHONE_NUMBER or edit the app.py user_phone variable in the App class to contain the "command phone".  **Must**
be formatted like '+1000000000'


### Starting the program:
To run TeXt-Top, run app.py (keep the commands folder as well)

### Texting a command:
To have a command activate on your computer, text the number you have chosen with the filename (no extension) you want to run. Some commands take arguments in addition to their name. These arguments must be comma separated. There are a few default commands, and you can add your own as you wish.

#### Included commands:
##### Linux:
1. download - Description: Downloads the file specified, Arguments: The url of the file you wish to download
2. find file - Description: Texts you back the directory of the file you specify, Arguments: The name of the file you would like to search for
3. get ip - Description: Texts you back the IP address of your computer, Arguments: None
4. lock - Description: Locks your screen, Arguments: None
5. restart - Description: Restarts your computer, Arguments: None
6. shutdown - Description: Shuts down your computer, Arguments: None
7. unlock - Description: Unlocks your locked computer, Arguments: None

##### Windows:
1. batman
2. capture
3. download
4. get dir
5. get ip
6. lock screen
7. restart
8. send mail
9. shutdown


### Creating a command:
You can write your own commands to be used by TeXt-Top in the form of either a Python script or a Shell script (others probably work as well). When writing your script, here are some general guidelines to keep in mind:

- The name of the script (minus the extension) will be the command name that you text.
- The arguments of your script become the comma-separated arguments when you text your command.
- Any printed statements in your code will be echoed as a text to the user, enabling you to customize the feedback to your phone.
- The exit status of the program determines the success/failure text that is sent back to the user.

Have fun!
