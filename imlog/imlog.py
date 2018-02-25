import os 
import re
import iso8601
import xml.etree.ElementTree as exml
import plistlib
import xml
import subprocess
import datetime
import sys

__all__ = ['IChatLog', 'AdiumLog']

class Message:
    """
    Cheap container class for all messages
    """

    def __init__(self):
        pass

    def __repr__(self):
        return("%s: %s" % (self.sender, self.text))

class IChatLog:
    def __init__(self, path):
        self.messages = []
        try:
            self.plist = plistlib.readPlist(path)
        except xml.parsers.expat.ExpatError:
            cmd = ['plutil', '-convert', 'xml1', '-o', '-', path]
            data = subprocess.check_output(cmd)
            self.plist = plistlib.readPlistFromString(data)
        
        self.objects = self.plist['$objects']
        self._set_service()

        for field in self.objects:
            if isinstance(field, dict):
                if 'ServiceLoginID' in field:
                    self.account = self.extract(field['ServiceLoginID'])

        for field in self.objects:
            if isinstance(field, dict):
                if 'MessageText' in field:
                    msg = Message()
                    send_id = self.extract(field['Sender'])
                    if send_id != '$null':
                        msg.sender = self.extract(send_id['ID'])
                        # ignore any weird senders
                        if isinstance(msg.sender, dict):
                            msg.sender = msg.sender['NS.string']
                        text = self.extract(field['MessageText'], 1)
                        if isinstance(text, dict):
                            if isinstance(text['NS.string'], unicode):
                                msg.text = text['NS.string'].encode('utf8')
                            else:
                                msg.text = text['NS.string']
                        else:
                            msg.text = text

                        secs = int(self.extract(field['Time'])['NS.time'])
                        nstime = datetime.datetime(2001, 1, 1)
                        msg.time = nstime + datetime.timedelta(0, secs)
                        self.messages.append(msg)

        # neccessary?
        self.messages.sort(key=lambda msg: msg.time)
        for x in self.messages:
            print(x)

    def _set_service(self):
        for field in self.objects:
            if isinstance(field, dict):
                if 'ServiceName' in field:
                    self.service = self.extract(field['ServiceName'])


    def extract(self, cfdict, offset=0):
        if 'CF$UID' in cfdict:
            return self.objects[int(cfdict['CF$UID']) + offset]

IChatLog(sys.argv[1])
