#!/usr/bin/python
import telepot
from datetime import datetime
import time
import os
import traceback
import requests
import json

# my modules
import robot_basics as rb
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


# check Internet connection by obtaining public IP
connected = False
while connected == False:
    try:
        req = requests.get("http://httpbin.org/ip")
        connected = True
        logWrite(0, "Connected to the Internet.")
    except Exception as Err:
        logWrite(3, "No Internet Connection." + str(traceback.format_exc()))
        time.sleep(30)

# keep on trying
while req.status_code != 200:
    time.sleep(30)
    req = requests.get("http://httpbin.org/ip")
    logWrite(2, "http status code: " + str(req.status_code))

# if request is "http 200" value is correct
if req.status_code == 200:
    # change the HTTP response body into a JSON type
    text = json.loads(req.text)
    # retreive value by key using dict
    ip = text['origin']
    logWrite(0, "IP pubblico: " + ip)

# create bot and insert token
tg_link = False
while tg_link == False:
    try:
        bot = telepot.Bot(token)
        user = bot.getMe()
        event = "Connection to Telegram successful! Bot user_id: " + str(user['id'])
        logWrite(0, event)
        tg_link = True
    except Exception as Err:
        logWrite(3, "Connection to Telegram failed.")
        logWrite(3, traceback.format_exc())

# activate default/custom keyboard
hide_kbd = {'hide_kbd': True}
show_kbd = {'keyboard': [['Motion ON', 'Snapshot', 'Motion OFF'],
                         ['Audio', 'DELETE ALL', 'Video'],
                         ['/\\'],
                         ['<<', '( | )', '>>'],
                         ['\\/'],
                         ['LOW', 'MEDIUM', 'HIGH']]
            }


# on message receive
def handle(msg):
    # assign message content and sender ID to function "glance()" (from telepot module)
    content_type, chat_type, chat_id = telepot.glance(msg)
    # sender's name and ID
    usr_name = msg['from']['first_name']
    usr_id = msg["from"]["id"]
    # authorized user
    adm_usr = int(admin)
    # verify content type (text required)
    if content_type == 'text':
        command = msg['text']
        # verify if the sender is an authorized user
        if usr_id != int(admin):
            # if not, log the event and send an alert to the admin
            message = 'Spiacente ' + usr_name + ', accesso non autorizzato. I tuoi dati saranno inviati ai miei amministratori.'
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
            elif command == "/delete" or command == "DELETE ALL":
                tgs.MediaDel()
                message = 'File multimediali eliminati.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Media deleted."
                print(event)
                logWrite(0, event)
                os.system('sudo pkill motion')
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
                tgs.Snapshot()

                # Robot movement controls
            elif command == "/forwards" or command == "/\\":
                rb.Forwards()
                message = 'Avanzo.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Moving robot forwards."
                print(event)
                logWrite(0, event)
            elif command == "/left" or command == "<<":
                rb.CntrClockwise()
                message = 'Sinistra.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Turning robot counterclockwise."
                print(event)
                logWrite(0, event)
            elif command == "/stop" or command == "( | )":
                rb.StopMotors()
                message = 'Mi fermo.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Motors stopped."
                print(event)
                logWrite(0, event)
            elif command == "/right" or command == ">>":
                rb.Clockwise()
                message = 'Destra.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Turning robot clockwise."
                print(event)
                logWrite(0, event)
            elif command == "/down" or command == "\\/":
                rb.Backwards()
                message = 'Retrocedo.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Moving robot backwards."
                print(event)
                logWrite(0, event)
            elif command == "/low" or command == "LOW":
                rb.Low()
                message = 'Velocità ridotta.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Low speed selected."
                print(event)
                logWrite(0, event)
            elif command == "/medium" or command == "MEDIUM":
                rb.Medium()
                message = 'Velocità media.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "Medium speed selected."
                print(event)
                logWrite(0, event)
            elif command == "/high" or command == "HIGH":
                rb.High()
                message = 'Velocità massima.'
                bot.sendMessage(chat_id, message, reply_markup=hide_kbd)
                event = "High speed selected."
                print(event)
                logWrite(0, event)
    else:
        # if message is not text, notify it to the sender.
        message = 'Mi spiace, non capisco. Scrivimi del testo.'
        bot.sendMessage(chat_id, message)

bot.message_loop(handle)

print ('Listening...\n')
while 1:
    time.sleep(1)
