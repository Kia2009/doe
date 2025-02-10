import requests
from bs4 import BeautifulSoup
import telebot
import os
from dotenv import load_dotenv


load_dotenv()


bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

def get_doe_details(url: str):

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }

        # Make request to the website
        response = requests.get(
            url,
            headers=headers
        )
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific div with class 'aq-number'
        aqi_div = soup.find('div', class_='aq-number')

        if aqi_div:
            # Extract and clean the number
            aqi_value = aqi_div.text.strip()
            return {
                'air_quality_index': aqi_value,
                'status': 'success'
            }
        else:
            return {
                'air_quality_index': None,
                'status': 'error',
                'message': 'AQI value not found'
            }

    except requests.exceptions.RequestException as e:
        return {
            'air_quality_index': None,
            'status': 'error',
            'message': f'Request failed: {str(e)}'
        }
    except Exception as e:
        return {
            'air_quality_index': None,
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    result = get_doe_details('https://www.accuweather.com/fa/ir/ahvaz/210047/air-quality-index/210047')
    bot.reply_to(message, "use 'شاخص' command to access the bot please")


@bot.message_handler(func=lambda message: message.text == "شاخص")
def handle_index_query(message):
    result = get_doe_details()
    if result['status'] == 'success':
        bot.reply_to(message, f"شاخص کیفیت هوای اهواز: {result['air_quality_index']}")
    else:
        bot.reply_to(message, "متاسفانه در دریافت اطلاعات مشکلی پیش آمده است.")

if __name__ == "__main__":
    try:
        print("Bot is running...")
        bot.infinity_polling()
    except Exception as e:
        print(f"Bot stopped due to error: {str(e)}")
    
