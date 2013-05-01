#! /usr/bin/env python
## -*- coding: utf-8 -*-
#
#  Do you like Python ?
#
#                          .-=-.          .--.
#              __        .'     '.       /  " )
#      _     .'  '.     /   .-.   \     /  .-'\
#     ( \   / .-.  \   /   /   \   \   /  /    ^
#      \ `-` /   \  `-'   /     \   `-`  /
#       `-.-`     '.____.'       `.____.'
#
#



""" Robinbot only talk with BatmanBot 
    
"""

from time import sleep
from datetime import datetime
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

class RobinBot(SingleServerIRCBot):
    cmd = ""
    message = []
    def __init__(self, channel, nickname, server, cmd, message, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.message = message
        self.cmd = cmd 

#   General    
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
#        c.privmsg("NickServ","identify RobinBot RobinIsFriendOfBatman")
        print "welcome"
        c.privmsg("BatmanBot", "With cmd : \""+self.cmd+"\"")
        for m in self.message: 
            print m
            sleep(1)
            c.privmsg("BatmanBot", m)

        self.connection.disconnect("Robin is friend of Batman")
        sys.exit(0)

    def on_privmsg(self, c, e):
        nick = nm_to_n(e.source())
        host = nm_to_h(e.source())
        said = e.arguments()[0]
        print host 

#    Validate
    def validate(self, str):
        ary=["import","os","shlex","command","subprocess","execl","open","login","urandom"]
        for exploit in ary:
            if exploit in str:
                return False
        return True

def main():
    server="irc.freenode.org"
    channel = "#ktmt.github" 
    nickname = "RobinBot" 
    cmd = " ".join(sys.argv[1:])
    print cmd 
    p = subprocess.Popen(sys.argv[1:], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.stdout.readlines()

    bot = RobinBot(channel, nickname, server, cmd, output)
    bot.start()

if __name__ == "__main__":
    main()

