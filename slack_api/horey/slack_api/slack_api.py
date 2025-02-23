"""
Shamelessly stolen from:
https://github.com/lukecyca/pyslack
"""
import pdb

import requests
import json
from horey.h_logger import get_logger
from horey.slack_api.slack_api_configuration_policy import SlackAPIConfigurationPolicy
from horey.slack_api.slack_message import SlackMessage

logger = get_logger()


class SlackAPIException(Exception):
    """ generic slack api exception
    """

    def __init__(self, *args, **kwargs):
        super(SlackAPIException, self).__init__(*args)

        self.error = kwargs.get("error", None)


class SlackAPI(object):
    def __init__(self, configuration: SlackAPIConfigurationPolicy = None):
        self.webhook_url = configuration.webhook_url

    def send_message(self, message: SlackMessage):
        logger.info(f"Sending message")

        response = requests.post(
            self.webhook_url, data=message.generate_send_request(),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                f'Request to slack returned an error {response.status_code}, the response is:\n{response.text}'
            )

        return True



