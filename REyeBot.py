#!/usr/bin/python
import tgSend as tgs

event = 'Motion detected: media acquired and sent to the admin.'
print(event)
tgs.logWrite(0, event)

tgs.MediaMove()
tgs.PicSend()
tgs.VideoSend()
tgs.AudioSend()
tgs.MediaDel()
