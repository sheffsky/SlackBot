import time
import ConfigParser
from SlackBot import SlackBot

Config = ConfigParser.ConfigParser()
Config.read("SlackConfig.ini")

slack_token = Config.get('SlackBotOptions', 'token')
test_channel_id = Config.get('SlackBotOptions', 'test_channel_id')
file_with_list = Config.get('EnvironmentOptions', 'list_file_path')


def main():
    slack_bot_dns320 = SlackBot(slack_token)

    #  getting the latest message timestamp
    msgs = slack_bot_dns320.get_sorted_latest_messages('', test_channel_id)
    if msgs:  # not empty
        ts = msgs[-1]['ts']
    else:
        ts = ''

    slack_bot_dns320.post_message('Ready. Type *help* to get started')

    while True:
        msgs = slack_bot_dns320.get_sorted_latest_messages(ts, test_channel_id)
        if msgs:  # not empty
            ts = msgs[-1]['ts']
            for msg in msgs:
                if 'bot_message' not in msg:
                    slack_bot_dns320.parse_command(msg['text'])
        time.sleep(5)

#  main()
# call('dir', shell=True)
# call('cmd.exe')

try:
    f = open(file_with_list, 'r+')
    for idx, item in enumerate(f):
        print idx, item.split(' ')[0].rjust(2), item.split(' ')[1].rjust(2), item.split(' ')[2].rjust(2)

except IOError as e:
    print('ERROR: ' + str(e))
