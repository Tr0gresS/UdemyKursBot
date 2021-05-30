
from telegram.ext import Updater, CommandHandler
import requests, re
from bs4 import BeautifulSoup



def udemy():
    response = requests.get("https://www.discudemy.com/feed/")
    if(response.status_code == 200):
        response_content = BeautifulSoup(response.content,"lxml")
        item =  response_content.select("channel > item > description >a")
     
        for j in item:
            url_code = j.get("href")
            
            first_index = url_code[26:]
            p = re.search("/",first_index)
            url_content = first_index[p.end():]
            response_coupon = requests.get(f"https://www.discudemy.com/go/{url_content}")
            
            response_coupon_content = BeautifulSoup(response_coupon.content,"lxml")
            url_coupon = re.search('<a href="(https://www.udemy.com/course.*) target=',str(response_coupon_content))
            content = url_coupon.group(1)
            
            return content
    else:
        print(response.status_code)


def start(update, context):
        son_kurs = None    
        while True:
            kurs = udemy()
            if kurs != son_kurs:
                son_kurs = kurs
                update.message.reply_text(son_kurs)
                print(son_kurs)


def main():
    token = "1897185958:AAFpW2U3hCPosA-qBsw13P80yBZFPsZlEe0"
    updater = Updater(token, use_context=True)
    komut = updater.dispatcher
    komut.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

      
if __name__ == "__main__":
    main()
    
    