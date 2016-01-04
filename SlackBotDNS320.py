import time
import ConfigParser
from operator import itemgetter

from SlackModule import SlackModule

Config = ConfigParser.ConfigParser()
Config.read("SlackConfig.ini")

slack_token = Config.get('SlackBotOptions', 'token')
test_channel_id = Config.get('SlackBotOptions', 'test_channel_id')


class SlackBot:
    __slack = ""
    username = 'dns_bot'
    icon_emoji = ':coffee:'
    channel = '#test'
    attachments = ""

    slack_command_prefix = 'slack_command_'

    def __init__(self, token):
        self.__slack = SlackModule(token)

    def get_sorted_latest_messages(self, stamp):
        params = {"channel": test_channel_id,
                  "oldest": stamp}
        try:
            result = self.__slack.call("channels.history", params)
            return_msgs = result.json()['messages']
            return sorted(return_msgs, key=itemgetter('ts'), reverse=False)
        except Exception as e:
            print e

    def post_message(self, text):
        parameters = {"channel": self.channel,
                      "text": text,
                      "username": self.username,
                      "parse": 'full',
                      "link_names": 1,
                      "attachments": self.attachments,
                      "icon_emoji": self.icon_emoji}
        self.__slack.call("chat.postMessage", parameters)

    def slack_command_help(self):
        """prints this help"""
        for slack_method in dir(self):
            if self.slack_command_prefix in slack_method and callable(getattr(SlackBotDNS320, slack_method)):
                self.post_message('*' + slack_method.replace(self.slack_command_prefix, '') + '* \n\t' +
                                  getattr(SlackBotDNS320, slack_method).__doc__)

    def slack_command_status(self):
        """hello out there"""
        self.post_message("hello out there!")

SlackBotDNS320 = SlackBot(slack_token)

#  getting the latest message timestamp
msgs = SlackBotDNS320.get_sorted_latest_messages('')
if msgs:  # not empty
    ts = msgs[-1]['ts']

SlackBotDNS320.post_message('Ready.')

while True:
    msgs = SlackBotDNS320.get_sorted_latest_messages(ts)
    if msgs:  # not empty
        ts = msgs[-1]['ts']
        for msg in msgs:
            if msg['text'] == 'help' and 'bot_message' not in msg:
                slack_command = SlackBotDNS320.slack_command_prefix + msg['text']
                if hasattr(SlackBotDNS320, slack_command) and callable(getattr(SlackBotDNS320, slack_command)):
                    getattr(SlackBotDNS320, slack_command)()
    time.sleep(5)
