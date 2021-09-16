# NPR Funding Credit Automation

This program automates the generation of an internal CapRadio spreadsheet containing cut numbers for NPR funding credits. 

---

## Features
- Automatically downloads pertinent NPR funding credit spreadsheets.
- Outputs an Excel Spreadsheet as well as to Google Sheets
- Integrates with Slack workspace in the form of a bot to trigger the funding credit update. This can be used by anyone with access to the channel with the bot.

---

## Requirements
1. Ubuntu Server 20.04
2. Python 3.8
4. Credentials to nprstations.org
5. [Google Service Account](https://cloud.google.com/docs/authentication/production#create_service_account) (for sheets integration)
6. Slack Workspace and Account (for Slack bot Integration)

---

## Environment Variables

These Environment variables should be stored in a `.env` file in ./modules/config/

### NPR Stations Website Credentials
- `USER_NAME={Username}`
- `PASSWORD={Password}`
- `NPR_ROOT={Root_URL}`
- `LOGIN_PAGE={Login_URL}`
- `CREDIT_PAGE={Funding_Credits_Page_URL}`

### Slack Credentials
- `SLACK_TOKEN={Token_from_Legacy_API}`

### Google Sheets
- `SPREADSHEET_ID={Google_Sheets_ID_String}`
- `TEST_ID={Google_Sheets_ID_String}`

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
- Execute `fund` with a `bot` flag
    ```
    $ . fund bot
    ```
- To trigger a new update `@mention` the bot's name along with one of the trigger strings. 
- The bot will notify you when the update is complete. 