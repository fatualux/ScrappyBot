#!/usr/bin/python
import telepot
from datetime import datetime
import os
import REyeConf as Conf

# IDs #
chat_id = Conf.chat_id
admin = Conf.admin
token = Conf.token


path = '/home/pi/motion/media/'
vid_path = path + 'Video/'
pic_path = path + 'Pictures/'
aud_path = path + 'Audio/'


# Return current date and time.
def now():
    ts = datetime.now()
    ts_sting = ts.strftime('%d-%m-%Y - %H:%M:%S')
    return ts_sting


# After the timestamp write the type of information it provides.
#   0 = [INF] information
#   1 = [AVV] alert
#   2 = [ERR] error
def logWrite(level, event):
    log = open("/home/pi/ScrappyBot/LOG", "a")  # open logfile in append mode
    string = now()  # write timestamp
    if level == 0:
        string = string + " [INF]"
    elif level == 1:
        string = string + " [ALR]"
    else:
        string = string + " [ERR]"
    string = string + " >>> " + event  # insert message

    log.write(string + "\n")  # append message to file
    log.close()  # close logfile


# create bot and insert token
bot = telepot.Bot(token)
user = bot.getMe()
event = "Connection to Telegram successful! Bot user_id: " + str(user['id'])
logWrite(0, event)
tg_link = True


def Snapshot():
    path = '/home/pi/motion/media/Pictures/'
    snap = path + 'Snapshot.jpg'
    take = 'raspistill -w 800 -h 600 -t 2000 -o ' + snap
    os.system(take)
    msg = "OK, ho scattato l'istantanea che mi hai chiesto."
    bot.sendMessage(chat_id, msg)
    PicSend()


def VideoRec():
    vid = vid_path + 'video.h264'
    recVid = 'raspivid -t 5000 -w 800 -h 600 -o ' + vid
    os.system(recVid)
    wrap = 'MP4Box -fps 30 -add ' + vid + ' ' + vid + '.mp4'
    os.system(wrap)
    os.system('rm ' + vid)


def AudioSend():
    voice = aud_path + 'voice.wav'
    cmd = 'arecord -D sysdefault:CARD=3 -d 10 -f cd -t wav ' + voice
    os.system(cmd)
    for filename in os.listdir(aud_path):
        content = open(os.path.join(aud_path, filename), 'rb')
        bot.sendAudio(chat_id, content)


def PicSend():
    for filename in os.listdir(pic_path):
        content = open(os.path.join(pic_path, filename), 'rb')
        bot.sendPhoto(chat_id, content)


def VideoSend():
    for filename in os.listdir(vid_path):
        content = open(os.path.join(vid_path, filename), 'rb')
        bot.sendVideo(chat_id, content)


def MediaMove():
    vid_move = 'mv ' + path + '*.avi ' + vid_path
    pic_move = 'mv ' + path + '*.jpg ' + pic_path
    os.system(vid_move)
    os.system(pic_move)


def MediaDel():
    rm_vid = 'rm ' + vid_path + '*'
    rm_pic = 'rm ' + pic_path + '*'
    rm_aud = 'rm ' + aud_path + '*'
    os.system(rm_vid)
    os.system(rm_pic)
    os.system(rm_aud)
