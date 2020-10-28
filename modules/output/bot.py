import os
from slack import WebClient
from slack import RTMClient
from modules.config.settings import SLACK_TOKEN, TARGET_SHEET
from modules.input.input_files import download_input_files
from modules.output.write import write


SLACK_CLIENT = WebClient(token=SLACK_TOKEN)
RTM_CLIENT = RTMClient(token=SLACK_TOKEN)

# websocket client
response = SLACK_CLIENT.rtm_connect(with_team_state=False)
intro_text = f"""\
*OPS-BOT* has been activated...

I can update the <https://docs.google.com/spreadsheets/d/{TARGET_SHEET}#gid=0|NPR Funding Credit Schdule> for you. 

*Just type:* `@ops-bot update NPR Funding Credit Schedule` to activate.
(or `@ops-bot funding`. That's much easier.)
    
    """
SLACK_CLIENT.chat_postMessage(
    channel='#ops-robot-test',
    text=intro_text
    )

_SELF_ID = response.get('self').get('id')
BOT_ID = f'<@{_SELF_ID}>'

TRIGGER_STRINGS = [
    "funder",
    "funders",
    "funding",
    "npr funding credits",
    "npr funding credit"
]


def download_and_update():
    download_input_files()
    write()


def send_task_confirmation(data, web_client=SLACK_CLIENT):
    user = data.get('user')
    channel = data.get('channel')
    confirmation_string = f"Hi <@{user}>!\nIt's updated."
    send_message(confirmation_string, channel, web_client)


def send_message(message_text: str, channel: str, web_client=SLACK_CLIENT):
    return web_client.chat_postMessage(channel=channel, text=message_text)


def run_bot():
    print('Starting Bot...')
    RTM_CLIENT.start()


@RTMClient.run_on(event="message")
def message_handler(**payload):

    data = payload.get('data')

    if BOT_ID not in data.get('text'):
        return

    message_text = data.get('text')

    for trigger in TRIGGER_STRINGS:
        if trigger in message_text.lower():
            download_and_update()
            web_client = payload.get('web_client')
            send_task_confirmation(data, web_client=web_client)
            return
