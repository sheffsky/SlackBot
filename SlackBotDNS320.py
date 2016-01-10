import time
import ConfigParser
from SlackBot import SlackBot

Config = ConfigParser.ConfigParser()
Config.read("SlackConfig.ini")

slack_token = Config.get('SlackBotOptions', 'token')
channel_id = Config.get('SlackBotOptions', 'channel_id')
file_with_list = Config.get('EnvironmentOptions', 'list_file_path')


def main():

    slack_bot_dns320 = SlackBot(slack_token, channel_id, file_with_list)

    #  getting the latest message timestamp
    msgs = slack_bot_dns320.get_sorted_latest_messages('')
    if msgs:  # not empty
        ts = msgs[-1]['ts']
    else:
        ts = ''

    slack_bot_dns320.post_message('Ready. Type *help* to get started')

    while True:
        msgs = slack_bot_dns320.get_sorted_latest_messages(ts)
        if msgs:  # not empty
            ts = msgs[-1]['ts']
            for msg in msgs:
                if 'bot_message' not in msg:
                    slack_bot_dns320.parse_command(msg['text'])
        time.sleep(5)

main()
