from operator import itemgetter
from SlackModule import SlackModule


class SlackBot:
    __slack_module = ""
    username = 'dns_bot'
    icon_emoji = ':coffee:'
    attachments = ""
    file_with_list = ""
    slack_command_prefix = 'slack_command_'
    channel = ""

    def __init__(self, token, channel, file_name):
        self.__slack_module = SlackModule(token)
        self.file_with_list = file_name
        self.channel = channel

    def get_sorted_latest_messages(self, stamp):
        params = {"channel": self.channel,
                  "oldest": stamp}
        result = self.__slack_module.call("channels.history", params)
        return_msgs = result.json()['messages']
        return sorted(return_msgs, key=itemgetter('ts'), reverse=False)

    def post_message(self, text):
        parameters = {"channel": self.channel,
                      "text": text,
                      "username": self.username,
                      "parse": 'full',
                      "link_names": 1,
                      "attachments": self.attachments,
                      "icon_emoji": self.icon_emoji}
        self.__slack_module.call("chat.postMessage", parameters)

    def slack_command_help(self):
        """prints this help"""
        for slack_method in dir(self):
            if self.slack_command_prefix in slack_method and callable(getattr(self, slack_method)):
                self.post_message('*' + slack_method.replace(self.slack_command_prefix, '') + '* \n\t' +
                                  getattr(self, slack_method).__doc__)

    def slack_command_print_file(self):
        """prints file"""
        try:
            f = open(self.file_with_list, 'r+')
            message = ""
            for idx, item in enumerate(f):
                message += '*' + str(idx) + '*: ' + item
            self.post_message(message)
            f.close()
        except IOError as e:
            self.post_message('ERROR: ' + str(e))

    def slack_command_delete_line(self, line_number):
        """deletes line in file
        :param line_number: line to delete
        """
        try:
            f = open(self.file_with_list, 'r+')
            lines = f.readlines()
            f.close()
            f = open(self.file_with_list, 'w')
            for idx, item in enumerate(lines):
                if int(line_number) != idx:
                    f.write(item)
            f.close()
            self.post_message('Line #{0} has been deleted.'.format(line_number))
        except IOError as e:
            self.post_message('ERROR: ' + str(e))

    @staticmethod
    def prepare_string_for_file(string):
        return string.replace('<', '').replace('>', '')

    def slack_command_add_line(self, string):
        """adds line to file
        :param string: line to add
        """
        try:
            f = open(self.file_with_list, 'a')
            f.write(self.prepare_string_for_file(string) + '\n')
            f.close()
            self.post_message('Done.')
        except IOError as e:
            self.post_message('ERROR: ' + str(e))

    def parse_command(self, command):
        slack_command = self.slack_command_prefix + command.split(' ')[0]
        slack_command_param = None
        if len(command.split(' ')) > 1:
            slack_command_param = command.split(' ', 1)[1]  # only one parameter is expected
        if hasattr(self, slack_command) and callable(getattr(self, slack_command)):
            try:
                if slack_command_param:
                    getattr(self, slack_command)(slack_command_param)
                else:
                    getattr(self, slack_command)()
            except TypeError as e:
                self.post_message('Error: ' + str(e))
