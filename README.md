# Gmail Job Enquiry Automator

## Overview
Fetches today's Gmail emails, filters for job enquiries, and sends them to Telegram using a Telegram bot.

## Setup
1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up Gmail API credentials (`credentials.json`) and run once to generate `token.json`.
3. Create a `.env` file with:
   ```env
   GMAIL_TOKEN_PATH=token.json
   GMAIL_CREDENTIALS_PATH=credentials.json

   ## Telegram
   TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
   TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

   ## Whatsup
   TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
   TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
   TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
   WHATSAPP_TO = os.getenv("WHATSAPP_TO") 
   ```
3. Create a Telegram bot with [@BotFather](https://t.me/botfather) and get your bot token.
4. Start a chat with your bot and get your chat ID using the getUpdates API.
5. Update `main.py` with your bot token and chat ID.


## Json to base64
[Convert]::ToBase64String([IO.File]::ReadAllBytes("Path to token.json")) | Out-File -Encoding ASCII "path to store token_base64.txt"               

## Usage
Run locally:
```bash
python main.py
```

## Deployment

Deploy as a scheduled job (e.g., on Render) to run every hour. 

