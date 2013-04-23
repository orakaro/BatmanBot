import re, math, sys, subprocess
from subprocess import Popen, PIPE
from cStringIO import StringIO
from time import sleep
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import ChatLog
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

import os
from BatmanBot import BatmanBot 

os.environ['PYTHONINSPECT'] = 'True'
