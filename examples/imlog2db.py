#!/usr/bin/env python

# Quick hack to generate a sqlite db of chat logs. 
# Currently used like so:
# find ~/Desktop/chatlogs -name "*.ichat" -exec python examples/imlog2db.py -d db.sqlite {} \;
# and so on..

import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../imlog')
import re
import imlog
import sqlite3
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('files', metavar='FILE', nargs="+")
parser.add_argument("-d" , dest="db", required=True)
args = parser.parse_args()

def init_log(path):
    if re.search("chatlog$", path):
        return imlog.AdiumLog(path)
    
    if re.search("ichat$", path):
        return imlog.IChatLog(path)

conn = sqlite3.connect(args.db)
cur  = conn.cursor()

cur.execute("select * from sqlite_master where type = 'table' and name = 'imlogs'")
if cur.fetchone() == None:
    cur.execute("""
        create table imlogs (
            sender text,
            txt text,
            t text
        )
    """)

sql = "insert into imlogs values (?, ?, ?)"
for path in args.files:
    log = init_log(path)
    for msg in log.messages:
        try:
            cur.execute(sql, (msg.sender, msg.text, msg.time))
            conn.commit()
        except sqlite3.InterfaceError:
            print msg.sender
            print msg.text
            print msg.time
