import requests
import os
from telegram import Bot
from telegram.error import TelegramError

bot = Bot(token=os.environ['BOT_TOKEN'])
chat_id = os.environ['CHAT_ID']
repo_url = 'https://raw.githubusercontent.com/metaloophole/meta-loophole-status/main'

def notify(text):
    try:
        bot.send_message(chat_id=chat_id, text=f'🪩 Loophole Bot:\n{text}', parse_mode='Markdown')
    except TelegramError as e:
        print(f'Telegram Error: {e}')

try:
    status = requests.get(f'{repo_url}/status.json').json()
except Exception as e:
    notify(f'*Failed to load status.json:* `{e}`')
    raise SystemExit()

if status.get('loophole_active') == True and status.get('region', '').lower() == 'usa':
    message = '⚠️ *Loophole ACTIVE for USA!*\nChange your PFP now 😈'

    method_req = requests.get(f'{repo_url}/method.txt')
    if method_req.status_code == 200 and method_req.text.strip():
        message += f'\n\n📄 *Method:*\n`{method_req.text.strip()}`'

    notify(message)
else:
    print('Loophole not active or not USA.')
