import os
from slack import WebClient
from slack import RTMClient
from funder.modules.config.settings import SLACK_TOKEN, TARGET_SHEET
from funder.modules.input.input_files import download_input_files
from funder.modules.output.write import write


class Ops_Bot:
    # TARGET_CHANNEL = '#ops-robot-test'
    TARGET_CHANNEL = '#operations'
    TRIGGER_STRINGS = [
    "funder", "funders", "funding"
    ]
    BOT_INTRO = f"""
    *OPSBOT* has been activated...

    I can update the <https://docs.google.com/spreadsheets/d/{TARGET_SHEET}#gid=0|NPR Funding Credit Schedule> for you. 

    *Just type:* `@opsbot update NPR Funding Credit Schedule` to activate.
    (or `@opsbot funding`. That's much easier.)
    """
    SHUTDOWN_MESSAGE = """*OPSBOT* deactivated..."""
    DEFAULT_EXT_FUNCS = (download_input_files, write)

    def __init__(self, token, external_functions=None):
        self.token = token
        self.external_functions = external_functions or self.DEFAULT_EXT_FUNCS

        self.web_client = WebClient(token=self.token)
        self.rtm_client = RTMClient(token=self.token)

        self.bot_id = self._connect()
        self.bot_id_text = f'<@{self.bot_id}>'

        # Decorate the message handler
        self.rtm_client.run_on(event='message')(self._message_handler)

    # @RTMClient.run_on(event='message')
    def _message_handler(self, **payload):

        data = payload.get('data')
        raw_message_text = data.get('text')

        if self.bot_id_text not in raw_message_text:
            return

        message_word_set = self._get_message_set(raw_message_text)

        if message_word_set.intersection(set(self.TRIGGER_STRINGS)):
            self._send_message("I'm on it!")
            try:
                self.run_external()
            except Exception as e:
                self._send_message(f"This is not going very well...\nERROR: {e}")
            self._send_task_confirmation(data)

    def start_bot(self):
        print('Starting Ops Bot...')
        self._introduce_yourself()
        try:
            self.rtm_client.start()
        except KeyboardInterrupt:
            print('Ops Bot Shutting Down...')
            self._send_message(self.SHUTDOWN_MESSAGE, self.TARGET_CHANNEL)
    
    def run_external(self):
        for func in self.external_functions:
            func()

    def _connect(self):
        response = self.web_client.rtm_connect(with_team_state=False)
        return response.get('self').get('id')

    def _introduce_yourself(self):
        self.web_client.chat_postMessage(
            channel=self.TARGET_CHANNEL,
            text=self.BOT_INTRO
        )

    def _send_task_confirmation(self, data):
        user = data.get('user')
        channel = data.get('channel')
        confirmation_string = f"OK <@{user}>!\nNPR Funding Credit Schedule is updated."
        self._send_message(confirmation_string, channel)

    def _send_message(self, message_text, channel=None):
        return self.web_client.chat_postMessage(channel=channel or self.TARGET_CHANNEL, text=message_text)

    def _process_message(self, input_text: str) -> str:
        return input_text.replace('\\xa0', '').lower()

    def _get_message_set(self, input_text: str) -> set:
        return set(self._process_message(input_text).split())


# main
def run_bot():
    bot = Ops_Bot(SLACK_TOKEN)
    bot.start_bot()