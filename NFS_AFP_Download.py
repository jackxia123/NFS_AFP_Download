# -*- coding: utf-8 -*-
"""
Spyder Editor

This is sync OS image script
#Author Jack Xia
"""
import os,schedule,smtplib
from  pyinotify import  WatchManager, Notifier, ProcessEvent,IN_DELETE, IN_CREATE,IN_MODIFY
from email.mime.text import MIMEText
from email.header import Header

nfsServerAddress = 'nfs-server.example.com'
afpServerAddress = 'afp-server.example.com'
osFileName='iOSSampleImage.dmg'
##File size 10G
filesize=2717687360

class EventHandler(ProcessEvent):
        """event handler"""
        def process_IN_CREATE(self, event):
                print   "Create file: %s "  %   os.path.join(event.path,event.name)

        def process_IN_DELETE(self, event):
                print   "Delete file: %s "  %   os.path.join(event.path,event.name)
    
        def process_IN_MODIFY(self, event):
                print   "Modify file: %s "  %   os.path.join(event.path,event.name)


#mount [-t vfstype] [-o options] device dir 
#-t vfstype file system，usually not nesscessary。mount right type automatically。 such as NFS
#-o options Mainly used to describe the way of mounting device or file。common parameters： such as rw： read/write method mount devices
#device (mounting device)
#dir (mount point)。
try:
var_nfs = os.system("mount -t nfs -o rw nfsServerAddress:/export/home/jack /mnt/nfs ")
var_afp = os.system("mount -t afp -o rw afpServerAddress:/export/home/jack /mnt/nfs ")
if var_nfs==256 || var_afp==256:
    print("Please make sure NFS server or AFP server running ok")
except:
    print("Failed to Mount NFS or AFP system")
    

def FSMonitor(path):   
        wm = WatchManager()
        mask = IN_DELETE | IN_CREATE |IN_MODIFY
        notifier = Notifier(wm, EventHandler())
        wm.add_watch(path, mask,rec=True)
        print 'now starting monitor %s'%(path)
                          

#Monitor iOSSampleImage.dmg whether exists between 07:00 pm and 09:00am              
def run():
nfsSchedule=schedule.every().day.at("19:00").to('09:00').do(FSMonitor(nfsServerAddress+'\\export\\home\\jack'+osFileName))
afpSchedule=schedule.every().day.at("19:00").to('09:00').do(FSMonitor(afpServerAddress+'\\export\\home\\jack'+osFileName))

if nfsSchedule || afpSchedule :
        try:
          ## rsync remote file to local host
          ## rsync [OPTION]... [USER@]HOST::SRC DEST
          #-z, --compress  compress the files when transferring。
          # -stats status of transferring files。
          #-b, --backup create backup file，It is for the purpose of existing have the same file name，rename the old file name to ~filename。Using--different prefix。
          #-a, --archive archive mode，，equalivent -rlptgoD。
          #-v, --verbose verbose files description
          #--progress display the progress of transferring。
          _thread.start_new_thread(os.system('rsync -abvz --progress root@192.168.78.192::nfsServerAddress/export/home/jack *'))
          _thread.start_new_thread(os.system('rsync -abvz --progress root@192.168.78.192::afpServerAddress/export/home/jack *'))
          SendEmail()
        except:
            print('Error:Can not start thread)
      else:
         #speedtest-cli --server=3633 --share 
         #--server=SERVER  server adress or Ip。
         #--share          share the test speed。
         #output afp and nfs server download speed
         nfsPattern=  commands.getoutput("speedtest-cli --server="+nfsServerAddress" --share")
         afpPattern= commands.getoutput("speedtest-cli --server="+afpServerAddress" --share") 
          
         nfsdownloadSpeed= re.match(r'Download /s* (/d*/./d+)/s+.*',nfsPattern).group(1)
         nfsdownloadSpeed= re.match(r'Download /s* (/d*/./d+)/s+.*',afpPattern).group(1)
         if nfsdownloadSpeed > nfsdownloadSpeed:
             #if nsf downloadspeed more than nfsdownload speed, start a thread to download
            _thread.start_new_thread.(os.system('rsync -abvz --progress root@192.168.78.192::nfsServerAddress/export/home/jack *'))
            SendEmail()
        else:
            #if afp downloadspeed more than nfsdownload speed, start a thread to download
            _thread.start_new_thread.(os.system('rsync -abvz --progress root@192.168.78.192::afpServerAddress/export/home/jack *'))
            SendEmail()

## Send Email with SMTP server          
def SendEmail():
    sender = 'LabUser@Apple.com' # send public User emails
    receivers = ['User@Apple.com']  # receiver User emails
    message = MIMEText('OSImage downloaded finished.', 'plain', 'utf-8')
    message['From'] = Header("LabUser", 'utf-8')     # Sender
    message['To'] =  Header("Kevin", 'utf-8')          # Receiver
    subject = 'OS Image Download Task'
    message['Subject'] = Header(subject, 'utf-8')
    try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print ("Send emails successfully")
    except smtplib.SMTPException:
    print ("Error: Can't send emails")
##Main function entry        
if __name__ == "__main__":
        run()                              