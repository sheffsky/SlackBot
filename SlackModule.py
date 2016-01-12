import requests


class SlackModule:
    slack_token = ""
    expected_code = 200

    def __init__(self, token):
        self.slack_token = token

    def __check(self, result_to_check):
        if result_to_check.status_code != self.expected_code:
            raise Exception(
                    "Expected code was " + str(self.expected_code) + ", but returned is " + str(
                        result_to_check.status_code))
        if not result_to_check.json()['ok']:
            raise Exception(
                    "Error! Server returned a message: " + result_to_check.json()['error']
            )

    def call(self, command, parameters):
        parameters.update({'token': self.slack_token})
        response = requests.post('https://slack.com/api/' + command,
                                 parameters)

        self.__check(response)

        return response
