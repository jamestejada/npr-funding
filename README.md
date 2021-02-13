# NPR Funding Credit Automation

This program automates the generation of an internal CapRadio spreadsheet containing cut numbers for NPR funding credits. 

---

## Features
- Automatically downloads pertinent NPR funding credit spreadsheets.
- Outputs an Excel Spreadsheet as well as to Google Sheets
- Integrates with Slack workspace in the form of a bot to trigger the funding credit update. This can be used by anyone with access to the channel with the bot.

---

## Requirements
1. ~~Windows 10~~ Ubuntu Server 20.04
2. Python 3.8
3. ~~Google Chrome Web Browser (used by Selenium/Helium)~~
4. Credentials to nprstations.org
5. Google Account (for sheets integration)
6. Slack Workspace and Account (for Slack bot Integration)

---

## Environment Variables

These Environment variables should be stored in a `.env` file in ./modules/config/

### NPR Stations Website Credentials
- ```USER_NAME={```Username```}```
- ```PASSWORD={```Password```}```
- ```LOGIN_PAGE={```Login URL```}```
- ```CREDIT_PAGE={```Funding Credits Page URL```}```

### Slack Credentials
- ```SLACK_TOKEN={```Slack Token from Legacy API```}```

### Google Sheets
- ```SPREADSHEET_ID={```Google Sheets ID String```}```
- ```TEST_ID={```Google Sheets ID String```}```

----

## Setup
1. Run `environ`
    ```
    $ . environ
    ```
    - This will create a python virtual environment and install libraries found in `requirements.txt`

2. Create a `.env` file in ./modules/config/ and populate with credentials listed above in the [Environment Variables](#environment-variables) section.

3. For Google Sheets integration:
    - Create a Spreadsheet in Google Sheets
    - Get the targeting string from the sheet url and enter it into the `.env` file.
    - The first time you run the program it will ask you to authenticate your Google account.

4. For Slack Integration:
    - Create a [Classic Slack App](https://slack.dev/python-slackclient/) (I know, I know...it's a legacy API)
    - After completing this process, enter the API token into the `.env` file.

5. Download sample `news.xls` and `newscast.xls` spreadsheets from nprstations.org, and modify tests to match. 

6. Run tests
    ```
    $ . fund tests
    ```


## Using this Program

### Manual Execution
- Simply execute the `fund` script. This has been provided at the top level directory for your convenience.
    ```
    $ . fund
    ```

### Running Slack Bot
- Execute `run.py` with a `bot` flag
    ```
    $ . fund bot
    ```
- To trigger a new update `@mention` the bot's name along with one of the trigger strings. 
- The bot will notify you when the update is complete. 