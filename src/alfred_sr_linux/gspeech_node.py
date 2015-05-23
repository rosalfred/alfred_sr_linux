#!/usr/bin/env python
# -*- coding: utf-8 -*-

PACKAGE='alfred_sr_linux'
NODE='system_speech'

PUB_SPEECH = 'speech'
PUB_CONFIDENCE = 'confidence'

import roslib; 
roslib.load_manifest( PACKAGE )
roslib.load_manifest( 'media_msgs' )
import shlex,subprocess,os,sys
import rospy

from media_msgs.msg import *
from std_msgs.msg import Int8

lang = 'fr-FR'
cmd1 = 'sox -r 16000 -t alsa default /tmp/recording.flac silence 1 0.3 1% 1 2.0 1%'
#cmd1='sox -r 16000 -t alsa hw:1,0 /tmp/recording.flac silence 1 0.2 5% 1 1.0 5%'
cmd2='wget -q -U "Mozilla/5.0" --remote-encoding=utf-8 --post-file /tmp/recording.flac --header="Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v1/recognize?client=chromium&lang=fr-FR"' # % (lang, ) # 

class SpeechNode( object ):
    """ """
    
    def __init__(self):
        rospy.init_node(NODE)
        pubs = rospy.Publisher( PUB_SPEECH, Command )
        pubc = rospy.Publisher(PUB_CONFIDENCE, Int8)
        
        args2 = shlex.split(cmd2)
        while not rospy.is_shutdown():
            os.system(cmd1)	
            output,error = subprocess.Popen(args2,stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
        
        rospy.loginfo( error )
        rospy.loginfo( output )
        
        if str( error ) == "Aborted.":
            sys.exit( 1 )
        
        if not error and len( output ) > 16:
            a = eval( output )
            rospy.loginfo( a )
            hypotheses = a['hypotheses']
            
            if hypotheses and len( hypotheses ) > 0:
                hypothese = hypotheses[0]
                confidence = float( hypothese['confidence'] )
                
                if confidence:
                    confidence = int( confidence * 100 )
                
                data = ( hypothese['utterance'] )
                rospy.loginfo( data )
                if data and data != "":
                    rospy.logdebug( "%s %s", str( data ), confidence )
                    
                    command = Command()
                    command.context = Context()
                    command.context.where = "/home/salon/"
                    command.context.who = "Mickael"
                    command.action = "say"
                    command.subject = data
                    
                    pubs.publish( command )
                    pubc.publish( confidence )
                    
                    if data == "arrêt du système":
                        sys.exit( 0 )
        
def run():
    try:
        SpeechNode()
    except rospy.ROSInterruptException, e:
        sys.exit(1) 
        pass
    #except KeyboardInterrupt:
    #    sys.exit(1)

if __name__ == '__main__':
    run()

