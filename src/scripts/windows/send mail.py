#This is the file used for sending emails with attachments.

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
import base64
from email import Encoders
from email.MIMEText import MIMEText
from subprocess import Popen, PIPE
import string, re, shlex,sys,smtplib, os

def send_mail(toadd='', body='This is a message sent from TeXt-Top', file_name=[], subject='A message sent from TeXt-Top.', fromnam='A TeXt-Top user'):
    
    #Make sure the user added a to address    
    if toadd=='':
        print "No address given to send to."
        return 1
    fromaddr="texttopcsc470@gmail.com"

    #Split the users going to receive a message into an array
    toaddr=toadd.split('/')

    #Gives the email messages detail
    msg = MIMEMultipart()
    msg['Subject'] = subject 
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)

    #If the number of wanted attachment files is not 0
    if not len(file_name)==0:
        
        #Split the files
        file_name=file_name.split('/')

        #For each file, attach it
        for i in range(0,len(file_name)):
            try:
                part = MIMEBase('application', "octet-stream")
                get_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'get dir.py'))
                #Change directory to location of the find file script
                p = Popen(['python', get_dir, file_name[i]], stdout=PIPE)
                output,errcode = p.communicate()
                filename = output.split('\n')[0].strip()
                print filename
                with open(filename, 'rb') as f:
                    part.set_payload(f.read())
                Encoders.encode_base64(part)

                #attach it
                part.add_header('Content-Disposition', 'attachment; filename='+filename)
                msg.attach(part)

            except IOError:
                print "The file: "+file_name[i]+' was not found.\n'


    msg_text=body+'\nFrom: '+fromnam

    #msg = MIMEText(msg_text)
    msg.attach(MIMEText(msg_text, 'plain'))

    #Connects to the gmail servers and sends the email.
    server = smtplib.SMTP()
    host="smtp.gmail.com"
    port="587"
    server.connect(host,port)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()

    #Logs the texttop email to the gmail servers.
    server.login("texttop.csc470@gmail.com", base64.b64decode("bWl0Y2hrb2JpbA=="))
    server.sendmail(fromaddr,toaddr, msg.as_string())
    server.quit()
    print "Message sent!"
    return 0

if __name__=="__main__":
    args = sys.argv[1:]
    if len(args) == 1:
        send_mail(args[0])
    elif len(args) == 2:
        send_mail(args[0], args[1])
    elif len(args) == 3:
        send_mail(args[0], args[1], args[2])
    elif len(args) == 4:    
        send_mail(args[0], args[1], args[2], args[3])
    elif len(args)==5:
        send_mail(args[0], args[1], args[2], args[3], args[4])    
    else:    
        send_mail()
