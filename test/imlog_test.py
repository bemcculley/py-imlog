import unittest
import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../imlog')
import imlog

fixtures = [
    ['adium_legacy','adium_aim.chatlog'],
    ['adium_aardvark','im.aardvark@gmail.com (2009-04-12T13.21.18-0400).chatlog'],
    ['ichat', 'lwmatthews3 on 2007-11-08 at 13.24.ichat'],
]

test_data = {}
for i in fixtures:
    test_data[i[0]] = os.path.dirname(__file__) + '/data/' + i[1]

class TestIMLog(unittest.TestCase):

    def setUp(self):
        pass

    def test_adium_legacy(self):
        log = imlog.AdiumLog(test_data['adium_legacy'])
        self.assertEqual(1, len(log.messages))
        msg = 'Your screen name (lwmatthews3) is now signed into AOL(R) Instant Messenger (TM) in 2 locations. To sign off the other location(s), reply to this message with the number 1. Click here for more information.'
        self.assertEqual(msg, log.messages[0].text)
        self.assertEqual('AIM', log.service)
        self.assertEqual('lwmatthews3', log.account)
        self.assertEqual('aolsystemmsg', log.messages[0].sender)

    def test_adium(self):
        log = imlog.AdiumLog(test_data['adium_aardvark'])
        self.assertEqual(2, len(log.messages))
        msg = "You there? I have a question about *government*  that I think you might be able to answer.(Type 'sure', 'pass', or 'busy'.)"
        self.assertEqual(msg, log.messages[0].text)
        msg = '<div><br><span style="font-family: Helvetica; font-size: 12pt;">Sorry I missed you.</span><br><span style="font-family: Helvetica; font-size: 12pt;">Type \'sure\' to see if you can answer the question, or ask something yourself!</span></div>'
        self.assertEqual(msg, log.messages[1].html)
        self.assertEqual('GTalk', log.service)
        self.assertEqual('dustym', log.account)

    def test_ichat(self):
        log = imlog.IChatLog(test_data['ichat'])
        self.assertEqual(1, len(log.messages))
        msg = 'http://pastie.textmate.org/private/joanrnq9fhsrl69k1e3ebw'
        self.assertEqual(msg, log.messages[0].text)
        self.assertEqual('dusty@curbed.com', log.account)
        self.assertEqual('AIM', log.service)

if __name__ == '__main__':
    unittest.main()