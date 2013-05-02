#! /usr/bin/env python
# -*- coding: utf-8 -*-
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

""" Batman bot listen and log all chat to sqlite and print out with commands
     
    Before reading this , remember that Batman Rocks The Gotham, and Python Rocks The World

    stats -- Prints some channel information.

    disconnect -- Disconnect the bot.  The bot will try to reconnect
                  after 60 seconds.

    die -- Let the bot cease to exist.

    dcc -- Let the bot invite you to a DCC CHAT connection.

    chatlog -- The bot will ask you provide date

    chatlog %Y-%m-%d -- print log chat 

    %Y-%m-%d -- print log chat 

    ** All calculator capable of Python Iteractive Shell (with no space)

"""

import re, math, sys, traceback
from time import sleep
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from table_def import ChatLog
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

class BatmanBot(SingleServerIRCBot):
    pyflg=True
    buf=[]
    safe_dict={}
    engine= None
    main=""
    def __init__(self, channel, nickname, server, main):
        SingleServerIRCBot.__init__(self, [(s, 6667) for s in server], main, nickname, nickname)
        self.channel = channel
        self.engine = create_engine('sqlite:///db/irclog.db', echo=True)
        self.main = main

#   SQLAlchemy
    def log(self, date, user, content):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        chatlog = ChatLog(date,user,content)
        session.add(chatlog)
        session.commit()

    def query(self, date):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        res = session.query(ChatLog).filter("strftime('%Y-%m-%d',date) =:qdate").params(qdate=date).all()
        return res

#   General    
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_dccmsg(self, c, e):
        c.privmsg("You said: " + e.arguments()[0])

    def on_dccchat(self, c, e):
        if len(e.arguments()) != 2:
            return
        args = e.arguments()[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def on_welcome(self, c, e):
        c.privmsg("NickServ","identify BatmanBot BatmanRockTheGotham")
        print "welcome"
        c.join(self.channel)

    def on_join(self, c, e):
        nick = nm_to_n(e.source())
        print "join"

#    Validate
    def validate(self, str):
        ary=["import","os","shlex","command","subprocess","execl","open","login","urandom"]
        for exploit in ary:
            if exploit in str:
                return False
        return True

    def bot_talking(self, nick):
        ignore_list = ["TaskBot"]
        if nick in ignore_list: return True
        return False

    def let_me_see_you(self, cmd):
        exec(cmd,{"__builtins__":None},self.safe_dict)
        keys=globals().keys()
        keys.remove('__doc__')
        keys.remove('__name__')
        keys.remove('__package__')
        keys.remove('__builtins__')
        scope={i:1 for i in keys}
        for i in scope:
            scope[i]=globals()[i]
        self.safe_dict=dict(self.safe_dict.items()+scope.items())

#    Private message
    def on_privmsg(self, c, e):
        nick = nm_to_n(e.source())
        ch = self.channel
        said = e.arguments()[0]
        self.one_param_command(c, e, said)

#    Listen on public message
    def on_pubmsg(self, c, e):
        ch = self.channel
        nick = nm_to_n(e.source())
        if self.bot_talking(nick): return
        try:
            chat = unicode(e.arguments()[0], "utf-8")
        except:
            chat = "### INVALID UTF-8 ###"
        if c.server == self.main: 
            try:
                self.log(datetime.now(),nick,chat)
                a = e.arguments()[0].split(":", 1)
                if len(a) > 1 and irc_lower(a[0].strip()) == irc_lower(self.connection.get_nickname()):
                    said = a[1].strip().split()
                    if not self.validate(a[1].strip()):
                        c.privmsg(ch, nick+": Haha I got you =)")
                        return
                    if len(said)==0: 
                        self.yessir(c, e)
                    elif len(said)==1:
                        cmd = said[0]
                        self.one_param_command(c, e, cmd)
                    elif len(said)>1:
                        if not self.pyflg:
                            cmd = said[0]
                            param = said[1]
                            self.many_param_command(c, e, cmd, param)
                        else:
                            self.one_param_command(c, e, a[1].strip())
                return
            except Exception, e:
                c.privmsg(ch, str(e))
                print traceback.format_exc()
        else: 
           print "live from co" 
           main_co = self.get_conn(self.main)
           main_co.privmsg(ch, chat)

    def get_conn(self,server_name):
        for key, value in self.conn.items():
            if key[0]==server_name:
                return value
        return None
    
#   Reply part
    def yessir(self, c, e):
        nick = nm_to_n(e.source())
        ch = self.channel
        c.privmsg(ch, nick+": Yes Sir ?")
        c.privmsg(ch, nick+": You can ask/privmsg me \"stats\" or \"chatlog %Y-%m-%d\" or \"dcc\" if want to chat dcc with me")
        c.privmsg(ch, nick+": Or do you just want to chat with a calculator :D")
         
    def said_you_said_me(self, c, e, cmd):
        nick = nm_to_n(e.source())
        ch = self.channel
        for chname, chobj in self.channels.items():
            mems=chobj.users()
        words=cmd.split()
        if cmd.lower()[:12]  == "do you think":
            if words[3] in mems:
                if words[3][:4] == "DTVD" or words[3] == "BatmanBot":
                    c.privmsg(ch, "Nope, man :D")
                else:
                    c.privmsg(ch, ": Yep of course"+cmd[12:])
            else:
                c.privmsg(ch, ": who is "+words[3]+" ?")
        elif cmd in ("hi","hello","Hi","Hello"):
            c.privmsg(ch, "Nice day "+nick)
        else:
            c.privmsg(ch, cmd)
 
    def rep_log(self, c, e, param):
        nick = nm_to_n(e.source())
        ch = self.channel
        res=self.query(param)
        c.privmsg(nick, "Total chat line: "+str(len(res)))
        c.privmsg(nick, "--- Chat Log Start ---")
        for r in res:
            sleep(1) 
            c.privmsg(nick,(r.date.strftime('%Y-%m-%d:%H:%M:%S')+" <"+r.user+"> "+r.content).encode('utf-8'))
        c.privmsg(nick, "--- Chat Log End ---")

    def one_param_command(self, c, e, cmd):
        nick = nm_to_n(e.source())
        ch = self.channel
        if cmd == "disconnect":
            self.disconnect()
        elif cmd == "die":
            self.die()
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.privmsg(nick, "--- Channel statistics ---")
                c.privmsg(nick, "Channel: " + chname)
                users = chobj.users()
                users.sort()
                c.privmsg(nick, "Users: " + ", ".join(users))
                opers = chobj.opers()
                opers.sort()
                c.privmsg(nick, "Opers: " + ", ".join(opers))
                voiced = chobj.voiced()
                voiced.sort()
                c.privmsg(nick, "Voiced: " + ", ".join(voiced))
        elif cmd == "dcc":
            dcc = self.dcc_listen()
            c.ctcp("DCC", nick, "CHAT chat %s %d" % (
                ip_quad_to_numstr(dcc.localaddress),
                dcc.localport))
        elif cmd == "chatlog":
            c.privmsg(ch, "Want to check the web first ? http://133.19.60.91:5000/irc/0 ")
            c.privmsg(ch, "Or not? Choose day and check private message (ex: \"2013-04-18\"): ")
        elif re.match(r'(\d{4}-\d{2}-\d{2})',cmd):
            param = cmd
            self.rep_log(c, e, param)
        elif cmd == "pythonmode":
            self.pyflg=True    
            c.privmsg(ch, "Welcome to "+cmd)
        elif cmd == "chatmode":
            self.pyflg=False    
            self.buf=""
            self.safe_dict={}
            c.privmsg(ch, "Welcome to "+cmd)
        else:
            try:
                self.let_me_see_you(cmd)
                rel=eval(cmd,{"__builtins__":None},self.safe_dict)
                c.privmsg(ch, rel)
            except:
                self.said_you_said_me(c, e, cmd)
                if self.pyflg: self.buf.append(cmd)

    def many_param_command(self, c, e, cmd, param):
        nick = nm_to_n(e.source())
        ch = self.channel
        if cmd == "chatlog":
            self.rep_log(c, e, param)

def main():
    server=["irc.freenode.org"]
    channel = "#ktmt.github" 
    nickname = ["BatmanBot"] 
    main = "irc.freenode.org"

    bot = BatmanBot(channel, nickname, server, main)
    bot.start()

if __name__ == "__main__":
    main()
