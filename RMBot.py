#!/usr/bin/python
import telepot
from datetime import datetime
import time
import os

# my modules
import RMBConf as Conf
import tgSend as tgs

# IDs #
admin = Conf.admin
token = Conf.token


# Return current date and time.
def now():
    ts = datetime.now()
    ts_sting = ts.strftime('%d-%m-%Y - %H:%M:%S')
    return ts_sting


def logWrite(level, event):
    # open logfile in append Mode
    log = open("/home/pi/ScrappyBot/LOG", "a")
    # write timestamp
    string = now()
    # After the timestamp write the type of information it provides.
    #   0 = [INF] information
    #   1 = [AVV] alert
    #   2 = [ERR] error
    if level == 0:
        string = string + " [INF]"
    elif level == 1:
        string = string + " [ALR]"
    else:
        string = string + " [ERR]"
    # insert message
    string = string + " >>> " + event + "\n"
    # append message to file
    log.write(string)
    # close logfile
    log.close()


# Put system boot into log file
logWrite(0, "System booted.")


# create bot and insert token
bot = telepot.Bot(token)
user = bot.getMe()
event = "Connection to Telegram successful!"
logWrite(0, event)
tg_link = True


# sender's name and ID
# authorized user
adm_usr = int(admin)
message = ">>> RMBOT AVVIATO <<<"
bot.sendMessage(adm_usr, message)
event = "System booted."
logWrite(1, event)


# activate default/custom keyboard
hide_kbd = {'hide_kbd': True}
show_kbd = {'keyboard': [['Motion ON', 'Motion OFF'],
                         ['Audio', 'Snapshot', 'Video'],
                         ['Delete All', 'REBOOT'],
                         ['POWEROFF']]
            }


# on message receive
def handle(msg):
    usr_name = msg['from']['first_name']
    usr_id = msg["from"]["id"]
    # assign message content and sender ID to function "glance()"
    content_type, chat_type, chat_id = telepot.glance(msg)
    # verify content type (text required)
    if content_type == 'text':
        command = msg['text']
        # verify if the sender is an authorized user
        if usr_id != int(admin):
            # if not, log the event and send an alert to the admin
            message = 'Spiacente ' + usr_name + ', accesso non autorizzato.'
            bot.sendMessage(chat_id, message)
            message = "Attenzione! L'utente " + usr_name + " (id " + str(usr_id) + ") ha scritto: <<" + command + ">>"
            bot.sendMessage(adm_usr, message)
            event = "Unauthorized user access! >>> " + usr_name.encode('utf-8') + " (id " + str(usr_id) + ") wrote: <<" + command.encode('utf-8') + ">>"
            logWrite(1, event)
        # if authorized, start the interaction
        else:
            if command == "/start" or command == "on":
                message = 'Ciao! Che posso fare per te?'
                bot.sendMessage(chat_id, message, reply_markup=show_kbd)
            elif command == "/motionon" or command == "Motion ON":
                message = 'Ho attivato il Guardian Mode.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Motion detection activated."
                print(event)
                logWrite(0, event)
                os.system('motion -b')
            elif command == "/motionoff" or command == "Motion OFF":
                os.system('sudo pkill motion')
                message = 'Ho disattivato il Guardian Mode.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Motion detection deactivated."
                print(event)
                logWrite(0, event)
            elif command == "/delete" or command == "Delete All":
                tgs.MediaDel()
                message = 'File multimediali eliminati.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Media deleted."
                print(event)
                logWrite(0, event)
                os.system('rm motion/media/Audio/*')
                os.system('rm motion/media/Video/*')
                os.system('rm motion/media/Pictures/*')
            elif command == "/videorec" or command == "Video":
                tgs.VideoRec()
                message = 'Registrazione video.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Video recorded."
                print(event)
                logWrite(0, event)
                tgs.VideoSend()
            elif command == "/audiorec" or command == "Audio":
                tgs.VideoRec()
                message = 'Registrazione audio.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Audio recorded."
                print(event)
                logWrite(0, event)
                tgs.AudioSend()
            elif command == "/snapnow" or command == "Snapshot":
                os.system('sudo pkill motion')
                message = 'Disattivo il Guardian Mode...'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Motion detection deactivated."
                print(event)
                message = 'Invio snapshot...'
                logWrite(0, event)
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                tgs.Snapshot()
                message = 'Ho riattivato il Guardian Mode.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Motion detection activated."
                print(event)
                logWrite(0, event)
                os.system('motion -b')
            elif command == "/reboot" or command == "REBOOT":
                message = 'Riavvio sistema.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Rebooting..."
                print(event)
                logWrite(0, event)
                os.system('sudo reboot')
            elif command == "/poweroff" or command == "POWEROFF":
                message = 'Spegnimento sistema.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Shutting down system."
                print(event)
                logWrite(0, event)
                os.system('sudo poweroff')
    else:
        # if message is not text, notify it to the sender.
        message = 'Mi spiace, non capisco. Scrivimi del testo.'
        bot.sendMessage(chat_id, message)


bot.message_loop(handle)

print('Listening...\n')
while 1:
    time.sleep(1)
