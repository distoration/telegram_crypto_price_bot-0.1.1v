import telegram.ext
import requests
import json
import time

print('bot is starting...')
time.sleep(2)

# enter below your telegram bot token you find in the "botfather".
bot_token = '6294200615:AAHVXsHoIrJ2znafkEqya_g2GY9Xf5OpquY'
updater = telegram.ext.Updater(token=bot_token, use_context=True)
print("API loaded correctly...") 

# function responsible for take by API coin price you want to get to know.
def get_price(symbol):
    url = f"https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        if "USD" in data:
            return data["USD"]
        else:
            return None
    else:
        return None

# function that takes your message from telegram e.g if you write /eth function takes it and send it to the symbol.
def handle_message(update, context):
    if update.message:
        message = update.message.text
        if message.startswith("/"):
            symbol = message.split(" ")[0][1:].upper()
            price = get_price(symbol)
            if price:
                chat_id = update.message.chat_id
                context.bot.send_message(chat_id=chat_id, text=f"{symbol} ${price}")
                print(f"{symbol} ${price}")
            else:
                chat_id = update.message.chat_id
                context.bot.send_message(chat_id=chat_id, text=f"Sorry, I couldn't find the coin you wrote, please write again correctly")
        else:
            pass

# main function.
# remember if bot at the start printing "Timed out, trying again..." please remove your bot from a telegram group. 
def main():
    dp = updater.dispatcher
    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
