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

Google Voice Edition

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
