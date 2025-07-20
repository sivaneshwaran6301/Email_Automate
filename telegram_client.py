import requests
from logs import logger

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    # logger.info("[TRACE] Sending Telegram message to chat_id %s;;;%s",bot_token, chat_id)
    response = requests.post(url, data=data)
    logger.info("[TRACE] Telegram API response: %s", response.text)
    return response.json() 