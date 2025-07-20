from gmail_client import authenticate_gmail, get_today_emails
from job_filter import is_job_enquiry
from telegram_client import send_telegram_message
from whatsapp_client import send_whatsapp_message
from logs import logger
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_BOT_TOKEN = TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = TELEGRAM_CHAT_ID

def main():
    service = authenticate_gmail()
    emails = get_today_emails(service)
    num_list_calls = 1  # One messages.list call
    num_get_calls = len(emails)  # One messages.get per email
    quota_units = num_list_calls * 5 + num_get_calls * 5
    logger.info("API calls: list=%d, get=%d, total=%d", num_list_calls, num_get_calls, num_list_calls + num_get_calls)
    logger.info("Quota units used: %d", quota_units)
    logger.info("Messages received: %d", len(emails))
    filtered_count = 0
    email_count = len(emails)
    for email in emails:
        logger.info("From: %s", email['from'])
        logger.info("Subject: %s", email['subject'])
        logger.info("Snippet: %s", email['snippet'])
        logger.info("Body: %s", email['body'])
        if is_job_enquiry(email):
            filtered_count += 1
            logger.info("[FILTERED] This email matches job enquiry keywords: %s", email['subject'])
            msg = f"Job Enquiry from {email['from']}:\nSubject: {email['subject']}\n\n{email['snippet']}"
            response = send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
            logger.info("[TELEGRAM] API response: %s", response)
            if response.get('ok'):
                logger.info("[TELEGRAM] Message sent successfully for: %s", email['subject'])
            else:
                logger.error("[TELEGRAM] Failed to send message for: %s", email['subject'])
        else:
            logger.info("[FILTERED] This email does NOT match job enquiry keywords: %s", email['subject'])
        
        # Uncomment the following lines to send WhatsApp messages
        # if is_job_enquiry(email):
        #     msg = f"Job Enquiry from {email['from']}:\nSubject: {email['subject']}\n\n{email['snippet']}"
        #     send_whatsapp_message(msg)
        #     print(f"Sent WhatsApp for: {email['subject']}")
    logger.info("Total emails processed: %d", email_count) 
    logger.info("Messages filtered as job enquiries: %d", filtered_count)

if __name__ == "__main__":
    main() 