#!/usr/bin/python
#
# irc bot using twisted
#

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol,ssl,task

import os
import time, sys
from optparse import OptionParser
import unicodedata
import ConfigParser

from irc_colors import Colors

     
#------------------------------------------------( functions / classes )


class Bot(irc.IRCClient):
    """ IRC bot."""
   
    def __init__(self,factory):
        self.factory=factory
        self.nickname = self.factory.nick
        self.password = self.factory.password
 

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)


    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.loop.stop()

    # callbacks for events
    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        for channel in self.factory.channelList:
            self.join(channel)
        
    def kickedFrom(self,channel,kicker,message):
        print "+ got kicked from: " + kicker + "\n"

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        #print "<%s> %s" % (user, msg)
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            if user == 'xxxx':
                msg = 'i know, i know, right?'
                self.msg(user, msg)
                return

        # Otherwise check to see if it is a message directed at me
        # if msg.startswith(self.nickname + ":"):
        #    msg = "%s: I am a  bot" % user
        #    self.msg(channel, msg)
        
        # handle commands
        if msg.startswith("!"):
            self.handleCommands(user,channel,msg)
        

    #def action(self, user, channel, msg):
    #    """This will get called when the bot sees someone do an action."""
    #    user = user.split('!')[0]
    #    print user
    
    # irc callbacks

    def irc_JOIN(self, user, params):
        """Called when a user joins a channel."""
        
        user = user.split('!')[0]
        channel=params[0]
        print "+ " + user + " joined channel " + channel
        
        #if its us, wave
        if user == self.nickname:
            self.describe(channel,'.o/') 
            return 1

        # print self.factory.usersToOp 
        if self.factory.usersToOp != []:
            if user in self.factory.usersToOp:
                self.mode(channel, True, 'o', user=user)
            else:
                #self.mode(channel, True, 'v', user=user)
                pass
       

    #def irc_NICK(self, prefix, params):
    #    """Called when an IRC user changes their nickname."""
    #    old_nick = prefix.split('!')[0]
    #    new_nick = params[0]
    #    print old_nick + " changed nick to: " + new_nick


    # override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname 
        that caused a collision in an effort to 
        create an unused related name for subsequent registration.
        """
        return nickname + '_'


    # other stuff
    def handleCommands(self,user,channel,msg):
        msg=msg[1:]
        print "[+] (cmd handler) got message: " + msg
        
        # help message
        if msg.startswith("help"):
            message=""
            message+="hey y0,\n"
            message+="commands are:\n"
            message+="!help     i'll print this message\n"

            self.msg(user,message.encode('utf-8'))

       
class BotFactory(protocol.ClientFactory):
    """A factory for Bots.

    A new protocol instance will be created 
    each time we connect to the server.
    """
    def __init__(self, channelList, usersToOp, nick, password):
        self.channelList = channelList
        self.usersToOp = usersToOp
        self.nick = nick
        self.password = password

    def buildProtocol(self,addr):
        b=Bot(self)
        return b

    def clientConnectionLost(self, connector, reason):
        #If we get disconnected, reconnect to server.
        connector.connect()


    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()



if __name__ == '__main__':            
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    
    parser.add_option("-s", "--server",action="store", type="string", dest="server")
    parser.add_option("-P", "--port",action="store", type="int", dest="port")
    parser.add_option("-c", "--channels",action="store", type="string", dest="channelList")
    parser.add_option("-S", "--ssl",action="store_true", default=False, dest="useSSL")
    parser.add_option("-o", "--op", action="store", type="string", dest="opedUsers", help="<user,resu> : nominate specific users joining a channel as ops") 
    parser.add_option("-m", "--mynick", action="store", type="string", dest="myNick")
    parser.add_option("-p", "--pass", action="store", type="string", dest="passwd")  
    (options, args) = parser.parse_args()
    
    # need server arg
    if not options.server:
        parser.error("need -s | --server <server>")
    # need port
    if not options.port:
        parser.error("need -P | --port <port>")
    # need channel arg
    if not options.channelList:
        parser.error("need -c | --channels <#channel1,#channel2>") 
   
    # channellist from commandline
    if options.channelList:
        channelList = options.channelList.split(',')

    #default nickname
    if options.myNick:
        myNick = options.myNick
    else:
        myNick = "hans"

    # password handling
    if options.passwd:
        passwd = options.passwd
    else:
        parser.error("need -p | --pass <password>")

    # op users from commandline
    if options.opedUsers:
        usersToOp = options.opedUsers.split(',')
    else:
        usersToOp = []
   

    # create factory protocol and application
    bot = BotFactory(channelList,usersToOp,myNick,passwd)
    
    # connect factory to this host and port
    if options.useSSL:
        reactor.connectSSL(options.server, options.port, bot,ssl.ClientContextFactory())
    else:
        reactor.connectTCP(options.server, options.port, bot)
       
    # run bot
    reactor.run()
    
