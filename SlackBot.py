from operator import itemgetter
from SlackModule import SlackModule


class SlackBot:
    __slack = ""
    username = 'dns_bot'
    icon_emoji = ':coffee:'
    channel = '#test'
    attachments = ""

    slack_command_prefix = 'slack_command_'

    def __init__(self, token):
        self.__slack = SlackModule(token)

    def get_sorted_latest_messages(self, stamp, channel):
        params = {"channel": channel,
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
            if self.slack_command_prefix in slack_method and callable(getattr(self, slack_method)):
                self.post_message('*' + slack_method.replace(self.slack_command_prefix, '') + '* \n\t' +
                                  getattr(self, slack_method).__doc__)

    def slack_command_status(self):
        """hello out there"""
        self.post_message("hello out there!")

    def parse_command(self, command):
        slack_command = self.slack_command_prefix + command
        if hasattr(self, slack_command) and callable(getattr(self, slack_command)):
            getattr(self, slack_command)()