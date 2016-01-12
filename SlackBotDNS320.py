import time
import ConfigParser
from SlackBot import SlackBot

Config = ConfigParser.ConfigParser()
Config.read("SlackConfig.ini")

slack_token = Config.get('SlackBotOptions', 'token')
channel_id = Config.get('SlackBotOptions', 'channel_id')
file_with_list = Config.get('EnvironmentOptions', 'list_file_path')


def main():

    timestamp = ''
    try:
        slack_bot_dns320 = SlackBot(slack_token, channel_id, file_with_list)
        #  getting the latest message timestamp
        msgs = slack_bot_dns320.get_sorted_latest_messages(timestamp)
        if msgs:  # not empty
            timestamp = msgs[-1]['ts']  # here it is
        slack_bot_dns320.post_message('Ready. Type *help* to get started')
    except Exception as e:
        print e

    while True:
        time.sleep(5)
        try:
            msgs = slack_bot_dns320.get_sorted_latest_messages(timestamp)
            if msgs:  # not empty
                timestamp = msgs[-1]['ts']
                for msg in msgs:
                    if 'bot_message' not in msg:
                        slack_bot_dns320.parse_command(msg['text'])
        except Exception as e:
            print e

main()
